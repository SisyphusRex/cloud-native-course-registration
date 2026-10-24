# AI Usage Disclosure: Claude Code session, 2026-10-24

This file records one working session with an AI coding assistant. It covers the
disclosure items required by the assignment for each major task, followed by a log
of every prompt in the session with a summary of the AI's response.

- **AI tool:** Claude Code (Anthropic), running the Claude Opus 5.5 model, used
  inside VS Code.
- **Branch:** `development`. Commits made in this session: `ae2a118` to `e2578cb`.
- **Responses are summarized**, not copied word for word. Prompts are quoted exactly
  as typed.

## Disclosure by task

### 1. Local dev server port in `wsgi.py`

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Understand why `app.run()` read the port from the `PORT` environment variable. |
| Sample Prompts | "in wsgi.py, why do we overcomplicate app.run() when we can just pass the port number, 8080, directly?"; "What sets the port env variable in the dockerfile?"; "So why are we using os.environ.get() in wsgi if running the app locally does not set the port variable?" |
| Generated Code Used | None directly. The AI suggested `app.run(host="127.0.0.1", port=8080)`; I made the edit to `wsgi.py` myself (commit `ae2a118`). |
| Verification Performed | Compared the explanation against the `Dockerfile` (`ENV PORT=8080` and the gunicorn `--bind 0.0.0.0:$PORT`). |

### 2. Blueprint structure: URL prefixes, keyword arguments, `MethodView`

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Decide where URL prefixes belong, make blueprint construction consistent, and convert the views to class-based `MethodView` resources. |
| Sample Prompts | "make each blueprint use kwargs. Also, move the urls to app.py so they are in one place."; "undo changing the urls"; "Move the prefixes to app.py."; "Can you reorganize the blueprints using MethodView? If the blueprint does not have all of the methods (get, post, put, delete) create stubs for them." |
| Generated Code Used | Yes. In `src/registration_api/`: the `url_prefix` arguments in `app.py`; the `IndexAPI`, `CoursesAPI` and `RegistrationAPI` classes with 501 stubs in `blueprints/index.py`, `blueprints/courses.py` and `blueprints/registration.py`. The comment above the registrations in `app.py` is my own. Commit `f4f4c5f`. |
| Verification Performed | Ran the existing pytest suite after each change (7 passed). Printed Flask's URL map to confirm `/`, `/courses` and `/register` were unchanged. Sent GET, POST, PUT and DELETE to each URL with Flask's test client to confirm real methods worked and stubs returned 501. |

### 3. Single-course resource and tests

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Add a `CourseAPI` resource at `/courses/<course_id>` with GET, PUT and DELETE, and test it. |
| Sample Prompts | "Could you make a plan to add another resource called CourseAPI at \"/<course_id>\"?"; "Don't implement the plan, just show me how courses.py would look."; "Make the change."; "Can you add the tests?" |
| Generated Code Used | Yes. `find_course()` and the `CourseAPI` class in `blueprints/courses.py`; 10 new tests and a fixture that restores the course catalog in `tests/test_app.py`. Commit `f4f4c5f`. |
| Verification Performed | Reviewed the planned code before approving it. Ran pytest (17 passed). Exercised each new endpoint with Flask's test client. Ran the delete test immediately before the list test to confirm the fixture reset works. |

### 4. Flask concepts (explanations only)

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Learn how Flask routing and class-based views work. |
| Sample Prompts | "why are the @blueprint.get() and @blueporint.post() prefereable to .route?"; "What does add_url_rule do in the blueprints?"; "Why do we need as_view again?"; "what are the arguments to add_url_rule"; "So in the current architecture, the app.py is the api, and each blueprint is an api endpoint, and within that endpoint there could be multiple classes with different logic depending on the url pattern?" |
| Generated Code Used | Example snippets only, not added to the project. The layer table from the last answer was saved to `docs/architecture.md` (commit `e8ac718`). |
| Verification Performed | The AI printed the `add_url_rule` signature from the installed Flask (3.1.3) rather than answering from memory. I checked the explanations against the code in the repository. |

### 5. Architecture diagram (Part A)

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Create the Part A diagram showing the client, REST API, Docker container and cloud platform. |
| Sample Prompts | "Could you create an architecture diagram showing the Client, REST API, Docker Container, and Cloud Platform per the ASSIGNMENT.md?"; "How did the https endpoint get into the diagram?"; "Simplify" |
| Generated Code Used | Yes. `docs/architecture-diagram.svg` and the rendered `docs/architecture-diagram.png`. Commit `046ac35`. |
| Verification Performed | The AI rendered the SVG with headless Chrome and inspected the image, fixing overlapping labels. I asked where the "HTTPS endpoint" box came from; the AI said it had added it from general knowledge of Cloud Run, not from the assignment, and I had it removed. The Artifact Registry deployment path is also the AI's assumption about how Cloud Run deployment works. |

### 6. Part A questions

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Understand the concepts behind Part A Q1 to Q3. |
| Sample Prompts | "why is this architecture considered cloud native?"; "what is K_Revision?"; "Which components are stateless?"; "How would the system scale?" |
| Generated Code Used | None. I wrote the answers in `docs/questions.md` myself, in my own words, based on these explanations (commit `e2578cb`). |
| Verification Performed | The AI tied each point to specific lines in the `Dockerfile` and source files, which I checked. It pointed out that the PUT and DELETE course endpoints make the course catalog stateful, which my draft answer to Q2 does not yet mention. |

### 7. Docker (Part B)

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Check the run command, fix a build warning, and learn container management commands. |
| Sample Prompts | "Is docker run -p 8080:8080 registration-api the correct command?"; "when i run docker build, i got this: ... JSONArgsRecommended ..."; "apply option 1"; "Is there a success message here?"; "how do i stop the container?" |
| Generated Code Used | Yes. The JSON-form `CMD ["sh", "-c", "exec gunicorn ..."]` and its comment in the `Dockerfile`. Commit `e127098`. |
| Verification Performed | The AI could not access Docker in its session, so it said its answers came from reading the `Dockerfile`. I rebuilt the image myself and confirmed the warning was gone. |

### 8. Repository housekeeping

| Item | Response |
|---|---|
| AI Tool(s) Used | Claude Code (Claude Opus 5.5) |
| Purpose | Ignore editor settings, write commit messages, and push. |
| Sample Prompts | "add .vscode to gitignore"; "commit and push" |
| Generated Code Used | The `.vscode/` line in `.gitignore` (commit `5b5bd48`) and the commit messages for this session. |
| Verification Performed | Checked `git status` and `git diff` before each commit, and confirmed each push reached `origin/development`. |

## Session log

Each prompt is quoted exactly. Responses are summarized.

1. **"in wsgi.py, why do we overcomplicate app.run() when we can just pass the port number, 8080, directly?"**
   The `app.run()` block only runs locally; in the container, gunicorn binds to `$PORT`. Reading `PORT` only allows overriding the local port. Suggested hard-coding 8080 and using `127.0.0.1`.
2. **"What sets the port env variable in the dockerfile?"**
   `ENV PORT=8080` sets a default in the image; Cloud Run (or `docker run -e`) overrides it at runtime. `EXPOSE` only documents the port. Noted an unfinished comment in the Dockerfile.
3. **"So why are we using os.environ.get() in wsgi if running the app locally does not set the port variable?"**
   Locally it always returns 8080 unless set by hand. The pattern was likely copied from Cloud Run samples, where `app.run()` is used in production. Recommended hard-coding it.
4. **"Is it a better practice to assign the url prefix to our blueprints in the app.py or how they are currently assigned?"**
   With one route per blueprint, full paths in decorators are fine. Prefixes in `app.py` help once a blueprint has several routes under one path.
5. **"make each blueprint use kwargs. Also, move the urls to app.py so they are in one place."**
   Changed all blueprints to `Blueprint(name=..., import_name=__name__)` and moved paths to `url_prefix` in `app.py`, using `""` routes to avoid trailing-slash redirects. Tests passed.
6. **"undo changing the urls"**
   Restored the full paths in the decorators and kept the keyword arguments. Tests passed.
7. **"Is assigning the blueprint url routes in the blueprint modules the best practice, or should they be in app.py?"**
   Routes belong in blueprint modules; only the shared prefix commonly goes in `app.py`.
8. **"Move the prefixes to app.py."**
   Moved the prefixes to `app.py` again with `""` routes. Tests passed and URLs were unchanged.
9. **"why are the @blueprint.get() and @blueporint.post() prefereable to .route?"**
   They are shortcuts for `.route(..., methods=[...])`: clearer, and you can't forget the method.
10. **"give me an example of the separate get() put() and delete() functions"**
    Showed separate view functions for `/courses/<course_id>` and the single-function alternative.
11. **"Is there a name for multiple methods vs a single method?"**
    No standard name; introduced Flask's class-based `MethodView` ("method-based dispatching").
12. **"Can you reorganize the blueprints using MethodView? If the blueprint does not have all of the methods (get, post, put, delete) create stubs for them."**
    Converted all three blueprints to `MethodView` classes with 501 stubs. Noted that unsupported methods now return 501 instead of 405. Tests passed.
13. **"What do we need to do to app.py?"**
    Nothing; `app.py` only registers blueprints.
14. **"What does add_url_rule do in the blueprints?"**
    It records a URL rule and view on the blueprint; `register_blueprint()` later applies the prefix and endpoint name.
15. **"Why do we use view_func=CoursesAPI ?"**
    We pass `CoursesAPI.as_view(...)`, which turns the class into a callable view; `view_func=` is a keyword because the second positional argument is `endpoint`.
16. **"remove passing the endpoint."**
    No endpoint argument is passed; the string in `as_view()` is a required name. Offered alternatives; no change made.
17. **"Why do we need as_view again?"**
    Flask can only call a function as a view; `as_view()` builds one that creates the class and dispatches by HTTP method.
18. **"what are the arguments to add_url_rule"**
    Listed `rule`, `endpoint`, `view_func`, `provide_automatic_options` and Werkzeug `Rule` options, from the installed Flask 3.1.3.
19. **"So the prefix in app.py determines which endpoint a request is routed too, and the url pattern in add_url_rule can be what function gets that request? but since we are using a class based view, the pattern is \"\" and the class handles the different requests?"**
    Clarified that prefix and rule combine into one URL that selects the view; `""` comes from the prefix layout, not from class-based views; the class selects the method.
20. **"Is it still appropriate to keep the prefixes in app.py?"**
    Yes; it fits resource-style classes. Optionally register the index blueprint without a prefix.
21. **"Could you make a plan to add another resource called CourseAPI at \"/<course_id>\"?"**
    Plan covering the class, registration, tests, fixture reset and design decisions.
22. **"Don't implement the plan, just show me how courses.py would look."**
    Showed the full proposed `courses.py` without changing files.
23. **"Make the change."**
    Implemented `CourseAPI`; existing tests passed and each new endpoint was exercised with the test client.
24. **"Can you add the tests?"**
    Added 10 tests and a fixture that restores the catalog. 17 tests passed.
25. **"commit and push"**
    Committed `ae2a118` (my `wsgi.py` change) and `f4f4c5f` (blueprints, `CourseAPI`, tests); left `.vscode/` uncommitted.
26. **"add .vscode to gitignore"**
    Uncommented the existing `# .vscode/` line in `.gitignore`.
27. **"commit and push"**
    Committed `5b5bd48`.
28. **"So in the current architecture, the app.py is the api, and each blueprint is an api endpoint, and within that endpoint there could be multiple classes with different logic depending on the url pattern?"**
    Corrected: a blueprint is a group of endpoints; each class is one endpoint tied to one URL pattern. Gave a layer table.
29. **"Could you save the table you just created in a file in docs/?"**
    Created `docs/architecture.md`.
30. **"commit and push"**
    Committed `e8ac718`.
31. **"Could you create an architecture diagram showing the Client, REST API, Docker Container, and Cloud Platform per the ASSIGNMENT.md?"**
    Created the SVG diagram and a PNG render, and fixed label overlaps after checking the render.
32. **"How did the https endpoint get into the diagram?"**
    The AI added it from general knowledge of Cloud Run; it is not in the assignment.
33. **"Simplify"**
    Removed the HTTPS endpoint box and put the service URL in the Cloud Run label.
34. **"Commit and push"**
    Committed `046ac35`.
35. **"why is this architecture considered cloud native?"**
    Containerized, managed serverless platform, horizontal autoscaling, configuration from the environment, small single-purpose service, disposable instances; in-memory state is the exception.
36. **"what is K_Revision?"**
    An environment variable Cloud Run (via Knative) sets to the name of the serving revision; the app returns it from `GET /`, defaulting to `"local"`.
37. **"Which components are stateless?"**
    The request path is stateless; the registrations list and, because of PUT and DELETE, the course catalog are per-instance state.
38. **"How would the system scale?"**
    Gunicorn threads within an instance and Cloud Run autoscaling across instances; in-memory state prevents correct scaling. Suggested aligning `--concurrency` with the thread count.
39. **"Is docker run -p 8080:8080 registration-api the correct command?"**
    Yes, given the image tag and `PORT=8080`. The AI could not access Docker, so this came from reading the Dockerfile.
40. **"when i run docker build, i got this: ... JSONArgsRecommended ..."**
    Explained the shell-form signal issue, why `exec` already handles it, and three options.
41. **"apply option 1"**
    Changed the `CMD` to `["sh", "-c", "exec gunicorn ..."]` with an explanatory comment.
42. **"remove the unfinished comment"**
    Removed the incomplete comment in the Dockerfile.
43. **"Is there a success message here?"**
    BuildKit prints no explicit success line; `FINISHED`, the step count and the image name show success. Suggested `docker images` and `--no-cache` for screenshots.
44. **"commit and push"**
    Committed `e127098`; left `docs/questions.md` uncommitted.
45. **"commit it too"**
    Committed `e2578cb`; noted that the Q2 draft omits the stateful course catalog, and a typo in Q1.
46. **"how do i stop the container?"**
    Ctrl+C in the foreground; otherwise `docker stop`. Explained `docker rm` and `--rm`.
47. **"how do i clear all containers listed in docker ps -a?"**
    `docker container prune` for stopped containers, or `docker rm -f $(docker ps -aq)` for all; images are not affected.
48. **"Could you record my prompts and your responses in a file under docs/ai_usage/ that fulfills the AI Usage Disclusure table in ASSIGNMENT.md?"**
    Created this file.
