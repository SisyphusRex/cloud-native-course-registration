#!/usr/bin/env python3
"""Part F, Test 3: send many simultaneous requests and watch Cloud Run scale.

Worker threads call GET / in a loop. Each response names the container
instance and revision that handled it, so the script prints a line whenever a
new instance starts answering, plus a status line every couple of seconds.
After the load stops it can also ask Cloud Monitoring how many instances
Cloud Run reported.

Requests to this API finish in a few milliseconds, so one instance with the
default concurrency of 80 rarely needs help. --concurrency temporarily lowers
the service's per-instance limit (which creates a new revision) so Cloud Run
has to add instances, and restores the original value when the test ends.

Usage:
    scripts/part_f_load_test.py --concurrency 1 --metrics
    scripts/part_f_load_test.py --url http://127.0.0.1:8080 --duration 20

Needs only the Python standard library, plus gcloud for --concurrency and
--metrics.
"""

# Standard Library imports
import argparse
import http.client
import json
import subprocess
import sys
import threading
import time
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone

DEFAULT_URL = "https://registration-api-bicubw576a-uc.a.run.app"
SERVICE = "registration-api"
REGION = "us-central1"
PROJECT = "cs6030-registration"


class Stats:
    """Results shared between the worker threads and the reporter."""

    def __init__(self):
        self.lock = threading.Lock()
        self.start = time.monotonic()
        self.requests = 0
        self.statuses = Counter()
        self.errors = Counter()
        self.per_instance = Counter()
        self.instance_revision = {}
        self.last_seen = {}
        self.new_instances = []  # (seconds since start, instance, revision)

    def record(self, status, body):
        now = time.monotonic() - self.start
        instance = revision = None
        if status == 200:
            try:
                info = json.loads(body)
                instance, revision = info["instance"], info["revision"]
            except (ValueError, KeyError):
                pass
        with self.lock:
            self.requests += 1
            self.statuses[status] += 1
            if instance:
                if instance not in self.per_instance:
                    self.new_instances.append((now, instance, revision))
                self.per_instance[instance] += 1
                self.instance_revision[instance] = revision
                self.last_seen[instance] = now

    def record_error(self, exc):
        with self.lock:
            self.requests += 1
            self.errors[type(exc).__name__] += 1


def worker(url, stop, stats):
    """Call GET / over one kept-alive connection until told to stop."""
    parts = urllib.parse.urlsplit(url)
    conn_class = (
        http.client.HTTPSConnection if parts.scheme == "https" else http.client.HTTPConnection
    )
    path = (parts.path.rstrip("/") or "") + "/"
    conn = None
    while not stop.is_set():
        try:
            if conn is None:
                conn = conn_class(parts.netloc, timeout=30)
            conn.request("GET", path)
            response = conn.getresponse()
            stats.record(response.status, response.read())
        except (OSError, http.client.HTTPException) as exc:
            stats.record_error(exc)
            if conn is not None:
                conn.close()
            conn = None
            time.sleep(0.2)
    if conn is not None:
        conn.close()


def report(stop, stats, interval):
    """Print new instances as they appear and a status line every interval."""
    printed_new = 0
    last_requests, last_time = 0, 0.0
    next_status = interval
    while not stop.wait(0.25):
        with stats.lock:
            new = stats.new_instances[printed_new:]
            printed_new = len(stats.new_instances)
            elapsed = time.monotonic() - stats.start
            requests = stats.requests
            seen = len(stats.per_instance)
            active = sum(1 for t in stats.last_seen.values() if elapsed - t < interval)
            not_ok = sum(n for code, n in stats.statuses.items() if code != 200)
            errors = sum(stats.errors.values())
        for t, instance, revision in new:
            print(f"[{t:6.1f}s] NEW INSTANCE {instance}  (revision {revision})", flush=True)
        if elapsed >= next_status:
            rate = (requests - last_requests) / (elapsed - last_time)
            print(
                f"[{elapsed:6.1f}s] {requests:6d} requests  {rate:6.1f} req/s  "
                f"instances active {active} / seen {seen}  non-200 {not_ok}  errors {errors}",
                flush=True,
            )
            last_requests, last_time = requests, elapsed
            next_status += interval
    # Instances that first answered after the last tick.
    with stats.lock:
        new = stats.new_instances[printed_new:]
    for t, instance, revision in new:
        print(f"[{t:6.1f}s] NEW INSTANCE {instance}  (revision {revision})", flush=True)


def gcloud(*args):
    result = subprocess.run(["gcloud", *args], capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout.strip()


def current_concurrency():
    return gcloud(
        "run", "services", "describe", SERVICE,
        "--region", REGION, "--project", PROJECT,
        "--format", "value(spec.template.spec.containerConcurrency)",
    )


def set_concurrency(value):
    print(f"Setting {SERVICE} concurrency to {value} (deploys a new revision)...", flush=True)
    gcloud(
        "run", "services", "update", SERVICE,
        "--region", REGION, "--project", PROJECT,
        "--concurrency", str(value), "--quiet",
    )


def instance_counts(start, end):
    """Return {minute: active instance count} from Cloud Monitoring, summed over revisions."""
    token = gcloud("auth", "print-access-token")
    query = urllib.parse.urlencode({
        "filter": (
            'metric.type="run.googleapis.com/container/instance_count" '
            f'AND resource.labels.service_name="{SERVICE}" '
            'AND metric.labels.state="active"'
        ),
        "interval.startTime": start.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "interval.endTime": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
    })
    request = urllib.request.Request(
        f"https://monitoring.googleapis.com/v3/projects/{PROJECT}/timeSeries?{query}",
        headers={"Authorization": f"Bearer {token}"},
    )
    with urllib.request.urlopen(request) as response:
        data = json.load(response)
    counts = Counter()
    for series in data.get("timeSeries", []):
        for point in series["points"]:
            counts[point["interval"]["endTime"]] += int(point["value"]["int64Value"])
    return dict(sorted(counts.items()))


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--url", default=DEFAULT_URL, help="base URL of the API")
    parser.add_argument("--threads", type=int, default=50, help="simultaneous clients (default 50)")
    parser.add_argument("--duration", type=float, default=60, help="seconds of load (default 60)")
    parser.add_argument("--interval", type=float, default=2, help="seconds between status lines")
    parser.add_argument(
        "--concurrency", type=int,
        help="temporarily set the service's per-instance concurrency to this value",
    )
    parser.add_argument(
        "--metrics", action="store_true",
        help="afterwards, wait for and print Cloud Monitoring instance counts",
    )
    args = parser.parse_args()
    url = args.url.rstrip("/")

    original = None
    if args.concurrency is not None:
        original = current_concurrency()
        set_concurrency(args.concurrency)

    try:
        print(f"Sending GET {url}/ from {args.threads} threads for {args.duration:.0f}s", flush=True)
        load_start = datetime.now(timezone.utc)
        stats = Stats()
        stop = threading.Event()
        threads = [
            threading.Thread(target=worker, args=(url, stop, stats), daemon=True)
            for _ in range(args.threads)
        ]
        reporter = threading.Thread(target=report, args=(stop, stats, args.interval))
        for thread in threads:
            thread.start()
        reporter.start()
        try:
            time.sleep(args.duration)
        except KeyboardInterrupt:
            print("\nStopping early...")
        stop.set()
        reporter.join()
        for thread in threads:
            thread.join(timeout=5)
        load_end = datetime.now(timezone.utc)
    finally:
        if original is not None:
            print(f"Restoring {SERVICE} concurrency to {original}...", flush=True)
            set_concurrency(original)

    elapsed = (load_end - load_start).total_seconds()
    print("\n=== Summary ===")
    print(f"Requests: {stats.requests} in {elapsed:.0f}s ({stats.requests / elapsed:.1f} req/s)")
    print("Status codes: " + ", ".join(f"{code}: {n}" for code, n in sorted(stats.statuses.items())))
    if stats.errors:
        print("Connection errors: " + ", ".join(f"{name}: {n}" for name, n in stats.errors.items()))
    print(f"Distinct instances that answered: {len(stats.per_instance)}")
    for instance, count in stats.per_instance.most_common():
        print(f"  {instance}  {count:6d} requests  (revision {stats.instance_revision[instance]})")

    if args.metrics:
        # Cloud Monitoring samples once a minute and publishes a few minutes late.
        wait = 180
        print(f"\nWaiting {wait}s for Cloud Monitoring to publish instance counts...", flush=True)
        time.sleep(wait)
        window_start = load_start - timedelta(minutes=1)
        window_end = load_end + timedelta(minutes=2)
        try:
            counts = instance_counts(window_start, window_end)
        except Exception as exc:  # noqa: BLE001 - report and carry on
            print(f"Could not read Cloud Monitoring: {exc}")
        else:
            print("Active instances per minute (Cloud Monitoring):")
            for minute, count in counts.items():
                print(f"  {minute}  {count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
