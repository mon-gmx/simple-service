# flask-simple-service
simple-service used to test some observability features in metrics exporter and otel

This is a simple Flask service that I use to learn how to emit metrics to prometheus, traces and spans to OTEL and logging using graylog (although the latter didn't work as I expected); this project was generated using Chat-GPT and my feedback.

The credentials are dummy values, so I don't care if a scrapper collects them, they have no use, but to my local lab

This is the prompt used to generate most of the code:

<pre>

I want a flask based service called simple_service running in port 5200, that has 3 endpoints:
1. An endpoint called "data", returns a random number using uuid4 if the request uses GET, or returns the data passed in the payload if the request uses POST.
2. An endpoint called "error" returns a random error from a list of possible errors: [400, 401, 404, 419, 429, 500, 503].
3. An endpoint called "metrics" this will return information about http requests and http response time from the two previous endpoints so it can be scrapped by prometheus. This will use prometheus client to emit the metrics.
The service using flask will log its operation using a log file that rotates every 10,000 lines or 3 days. The logging uses a greylog format (GELF).
The service will write requests into a database where it will insert the request IP, endpoint, method and response code in a table called requests. The models for the database will be written using dataclasses
The database exists in postgres with the name simpleservice (user simpleserviceuser, password simpleservicepw11; use pyscopg2 driver. The database will be migrated using alembic and connections will be created using SQLAlchemy. I need a migration script for the database intialization and the commands to start alembic and to migrate if anything changes.
The service will import the configuration from an object. The object will have a development and test configurations, the service can be run either as test or as development(default) and load the correct configuration.
There will be unit tests using pytest where the configuration will allow us to use a different driver for testing, using SQLite and a mock with a function scope per unit test.
Open telemetry will run in this service, making spans and tracing available for requests in this service so we can trace execution time in any part of the system.
</pre>

This service works with Jaeger and Prometheus, you will need a scrapper and a database in postgres but so far everything is working.

I added in the latest update another downstream to test requests and instrumentation to push data into honeycomb. This wasn't done using Chat-GPT but the prompt should be quite simple to do for generating both the call and the tests. The downstream call was added into the `/data` call, nothing fancy, the remote service should return a string, for testing I just created another service with a call to random: ```''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))```
