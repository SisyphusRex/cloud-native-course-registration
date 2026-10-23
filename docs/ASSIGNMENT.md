# CS6030 Assignment 2

## Building and Deploying a Cloud-Native Course Registration Microservice on Google Cloud

| | |
|---|---|
| **Course** | CS6030 – Cloud Computing and Cloud-Native Application Development |
| **Points** | 100 |
| **Type** | Individual Assignment |
| **Estimated Time** | 5–6 Hours |
| **AI Tools** | Allowed with Disclosure |
| **Cloud Budget** | ≤ $25 Google Cloud Credits |

## Assignment Overview

In this assignment, you will design, containerize, deploy, test, and evaluate a simple cloud-native
microservice on Google Cloud Platform (GCP).

Implement a Course Registration API that allows querying available courses and registering
students.

The assignment integrates concepts from:

- Virtual Machines
- Infrastructure Services
- Containers vs VMs
- Docker
- Resource Isolation
- Cloud Platforms
- Twelve-Factor Applications
- Stateless Services
- Scalability
- Resilience
- REST APIs
- Microservices

## Scenario

WMU's Computer Science Department wants a lightweight cloud-native version of its course
registration system.

The first version should:

1. Provide course information through an API.
2. Allow students to register for courses.
3. Be packaged as a Docker container.
4. Run in Google Cloud.
5. Demonstrate cloud-native design principles.

## Learning Outcomes

Upon successful completion, students will be able to:

- Deploy a containerized application on GCP
- Explain differences between VMs and containers
- Build a Docker image
- Deploy a cloud-native application
- Implement REST APIs
- Apply stateless service principles
- Use generative AI tools responsibly

## Technical Requirements

Students will build a simple REST API.

### Required Endpoints

#### View all courses

`GET /courses`

Response:

```json
[
  {
    "id": "CS6030",
    "title": "Cloud Computing"
  }
]
```

#### Register for a Course

`POST /register`

Request:

```json
{
  "student": "John Smith",
  "course": "CS6030"
}
```

Response:

```json
{
  "status": "registered"
}
```

### Technology Stack

Students may choose:

| Language | Framework |
|---|---|
| Python | Flask or FastAPI |
| JavaScript | Node.js + Express |

## Part A – Architecture Design (15 pts)

Create an architecture diagram showing:

- Client
- REST API
- Docker Container
- Cloud Platform

### Questions

- **Q1** Why is this architecture considered cloud-native?
- **Q2** Which components are stateless?
- **Q3** How would the system scale?

## Part B – Containerization (25 pts)

Create a Dockerfile.

Example:

```dockerfile
FROM python:3.12
COPY . /app
WORKDIR /app
RUN pip install flask
CMD ["python","app.py"]
```

### Required Deliverables

| | Command |
|---|---|
| **Build** | `docker build -t registration-api .` |
| **Run** | `docker run -p 8080:8080 registration-api` |

Submit screenshots showing:

- Build success
- Running container
- API accessible

## Part C – Deploy to Google Cloud Run (25 pts)

Deploy the application using Google Cloud Run.

Cloud Run is recommended because:

- Container based
- Serverless
- Free tier available
- Fits within assigned cloud credits

Typical cost for this assignment: less than $2 when resources are deleted afterward.

### Required Steps

Deploy with `gcloud run deploy` or through GCP Console.

### Deliverables

Submit:

- Cloud Run service URL
- Screenshot of deployment
- Screenshot of successful API response

## Part D – Cloud-Native Evaluation (15 pts)

Evaluate the application against cloud-native principles.

### Twelve-Factor Review

Answer:

1. Is configuration separated from code?
2. Is the service stateless?
3. Could multiple copies run simultaneously?
4. Does it store user state locally?

### Example

Bad:

```python
student_list = []
```

stored only in memory

Explain why.

## Part E – VM versus Container Analysis (10 pts)

Suppose the API receives:

| Period | Load |
|---|---|
| Normally | 20 users/day |
| During registration | 10,000 users/day |

Answer:

- **Q1:** Would you deploy this on a VM or a container platform?
- **Q2:** What advantages does a container provide?
- **Q3:** How would scaling differ?

## Part F – Testing and Resilience (10 pts)

Perform testing.

| Test | Description |
|---|---|
| **Test 1** | GET request: `GET /courses` |
| **Test 2** | POST request: `POST /register` |
| **Test 3** | Launch multiple browser tabs and issue requests simultaneously. You could be creative and write scripts to accomplish this task. |

**Question:** Could multiple instances of your application serve these requests? Explain.

## AI Usage Disclosure (Required)

Students must provide for each major task:

| Item | Response |
|---|---|
| AI Tool(s) Used | |
| Purpose | |
| Sample Prompts | |
| Generated Code Used | |
| Verification Performed | |

## Submission

Submit a PDF report which contains:

- Architecture diagram
- Screenshots
- Answers
- Discussion
- AI disclosure

### Source Files

A zip file containing:

- `app.py`
- `requirements.txt`
- `Dockerfile`

## Bonus Challenge (+10 pts)

Implement a second microservice:

`GET /students`

Deploy it separately on Cloud Run.

Create a simple architecture:

- Student Service
- Course Service

and explain why this is a microservices architecture.

## Grading Rubric

| Component | Points |
|---|---|
| Architecture Design | 15 |
| Containerization | 25 |
| Cloud Run Deployment | 25 |
| Cloud-Native Evaluation | 15 |
| VM vs Container Analysis | 10 |
| Testing & Resilience | 10 |
| **Total** | **100** |
