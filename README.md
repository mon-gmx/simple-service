# flask-simple-service
simple-service used to test some observability features in metrics exporter and otel

This is a simple Flask service that I use to learn how to emit metrics to prometheus, traces and spans to OTEL and logging using graylog (although the latter didn't work as I expected); this project was generated using Chat-GPT and fixed by me.

The credentials are dummy values, so I don't care if a scrapper collects them, they have no use, but to my local lab

This is the prompt used to generate most of the code:

This service works with Jaeger and Prometheus, you will need a scrapper and a database in postgres but so far everything is working.

I added in the latest update another downstream to test requests and instrumentation to push data into honeycomb. The downstream call was added into the `/data` call, nothing fancy, the remote service should return a string, for testing I just created another service with a call to random: ```''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))``` If you there's no downstream, it can use the `/random` endpoint in this project.
