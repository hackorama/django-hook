# Deploy with Docker


## Docker Compose

For quick demo docker compose is the best option.

### Use published images from docker hub

```shell script
$ docker-compose up
Pulling hooks (hackorama/hooks:)...
Pulling consumer (hackorama/consumer:)...
consumer_1  | Starting webhook consumer at http://127.0.0.1:8888/
hooks_1     | Starting Hooks Django server at http://localhost:8000/ ...
...
hooks_1     | Adding webhook "Logging" (http://consumer:8888/logging) with payload "{'event': 'read', 'time': '2020-05-06T08:49:09.930594'}" to task queue
consumer_1  | Received POST /logging {"event": "read", "time": "2020-05-06T08:49:09.930594"}, Responded with 200

```

### Or build local images and run

```shell script
$ docker-compose -f docker-compose-dev.yaml up
Building hooks
Building consumer
consumer_1  | Starting webhook consumer at http://127.0.0.1:8888/
hooks_1     | Starting Hooks Django server at http://localhost:8000/ ...
...
```


## Docker

For dev and test scenarios Docker can be used directly for flexibility.

### Run the image from docker hub

On docker hub: [hackorama/hooks](https://hub.docker.com/r/hackorama/hooks)

```shell script
$ docker run -d --name=hooks -p 8000:8000 -p 8888:8888 hackorama/hooks
```

> NOTE: Default Django admin credentials are `admin/admin` for hooks Docker image

### Or build a local image and run

```shell script
$ docker build -t hooks .

$ docker images | grep hooks
hooks                                  latest              1d1aefbd1bf1        11 hours ago        963MB

```

```shell script
$ docker run -d --name=hooks -p 8000:8000 -p 8888:8888 hooks

$ docker ps  | grep hooks
22aa8a5a45ca  hooks "/server/entrypoint.…"  8 minutes ago   Up 8 minutes   0.0.0.0:8000->8000/tcp   hooks
```

```shell script
$ docker logs hooks --follow
...
Huey task queue worker started with logs at /server/hey.log
...
Starting Hooks Django server at http://localhost:8000/ ...
...
Adding webhook "Alerts" (http://localhost:8888/alerts) with payload "{'event': 'create', 'time': '2020-04-09T08:51:48.381993'}" to task queue
[2020-04-09 08:51:56,695] INFO:huey:Worker-1:Added task 2bb6a2bf-cb1a-4d04-aa8a-1cf0c1581f55 to schedule, eta 2020-04-09 15:51:59.694755
Requesting POST http://localhost:8888/alerts {'event': 'create', 'time': '2020-04-09T08:51:48.381993'}
...

```

Test consumer is provided in the image and can be run as follows 

```shell script
$ docker exec -ti hooks bash
root@22aa8a5a45ca:/server# python /server/consumer.py
Starting webhook consumer at http://127.0.0.1:8888/
...
Received POST /alerts {"event": "create", "time": "2020-04-09T08:51:48.381993"}, Responded with 200

```

### Test

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) on browser to access the server.

See [the tests page](tests.md) on how to use test consumer and test the webhook execution.

![Main web page](screenshots/webhook-app.png)

Open [http://127.0.0.1:8888](http://127.0.0.1:8888) on browser to access the test consumer.

![Test consumer](screenshots/consumer.png)



## TODO

- Split Django and Huey process into separate Docker images
  - Add a shared volume for using the same SQLite database for Django and Huey images
