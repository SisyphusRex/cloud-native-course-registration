# Part A Architecture Design
## Questions
1. Why is this architecture considered cloud-native?
The architecture is considered cloud-native because it is packaged as a container, in runs on google cloud run, its configuration comes from the environment, and it scales horizontally.
2. Which components are stateless?
Everything is stateless except for the POST requests to register.  That saves a course to an in memory list which is unique to each instance.
3. How would the system scale?
There are two ways to scale: within an instance and across instances.  Gunicorn allows multiple threads within a container instance to handle simultaneous requests.  Cloud run autoscaling creates more instances when the running instances hit their "concurrency" limit.