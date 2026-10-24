# API architecture

How the Flask pieces in `src/registration_api/` fit together.

| Layer | In the code | What it is |
|---|---|---|
| **API (application)** | `app` in [app.py](../src/registration_api/app.py) | The whole service. `app.py` creates it and decides where each blueprint is mounted. |
| **Blueprint** | `courses_bp` | A group of related endpoints under one prefix, such as everything about courses. |
| **Endpoint / resource** | `CoursesAPI` at `/courses`, `CourseAPI` at `/courses/<course_id>` | One URL pattern, handled by one view class. Flask's endpoint names are `courses.list_courses` and `courses.course`. |
| **Operations** | `get()`, `put()`, `delete()` on a class | What you can do to that resource. The class picks the method from the HTTP verb. |

For example, `courses_bp` contains two endpoints, each with its own class and URL pattern:

```
courses_bp  (mounted at /courses by app.py)
├── ""             → CoursesAPI  (the collection)
└── "/<course_id>" → CourseAPI   (one course)
```

The URL pattern picks the class, and the HTTP method picks the function inside it.
