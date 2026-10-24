#!/usr/bin/env bash
# Part F, Tests 1 and 2: send GET /courses and POST /register to the API and
# check the status codes.
#
# Usage: scripts/part_f_tests.sh [BASE_URL]
#   BASE_URL defaults to the deployed Cloud Run service. Pass
#   http://127.0.0.1:8080 to test a local run instead.

set -u

API="${1:-https://registration-api-bicubw576a-uc.a.run.app}"
API="${API%/}"
failures=0

# request METHOD PATH EXPECTED_STATUS [JSON_BODY]
# Prints the request, status, and response body, and records a failure when
# the status doesn't match.
request() {
    local method="$1" path="$2" expected="$3" body="${4:-}"
    local args=(-s -X "$method" -w '\n%{http_code}')
    if [[ -n "$body" ]]; then
        args+=(-H "Content-Type: application/json" -d "$body")
    fi

    local output status
    output=$(curl "${args[@]}" "$API$path")
    status="${output##*$'\n'}"
    RESPONSE="${output%$'\n'*}"
    RESPONSE="${RESPONSE%$'\n'}" # Flask ends JSON responses with a newline

    echo "> $method $path ${body:+$body}"
    echo "< $status"
    if [[ "$status" == "$expected" ]]; then
        echo "PASS (expected $expected)"
    else
        echo "FAIL (expected $expected)"
        failures=$((failures + 1))
    fi
}

echo "Testing $API"

echo
echo "=== Test 1: GET /courses ==="
request GET /courses 200
count=$(python3 -c 'import json, sys; print(len(json.load(sys.stdin)))' <<<"$RESPONSE" 2>/dev/null)
echo "Courses returned: ${count:-could not parse response}"
echo "First course: $(python3 -c 'import json, sys; print(json.load(sys.stdin)[0])' <<<"$RESPONSE" 2>/dev/null)"

echo
echo "=== Test 2: POST /register ==="
request POST /register 201 '{"student": "John Smith", "course": "CS6030"}'
echo "Body: $RESPONSE"

echo
echo "--- Invalid registrations are rejected ---"
request POST /register 400 '{"course": "CS6030"}'
echo "Body: $RESPONSE"
request POST /register 404 '{"student": "John Smith", "course": "CS9999"}'
echo "Body: $RESPONSE"

echo
if ((failures == 0)); then
    echo "All checks passed."
else
    echo "$failures check(s) failed."
fi
exit $((failures > 0))
