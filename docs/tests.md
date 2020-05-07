# Tests and Coverage

- [Automated unit tests and coverage](#automated-unit-tests-and-coverage)
- [Manual integration tests](#manual-integration-tests)

## Automated unit tests and coverage

Basic API tests added with code coverage enabled using [Nose](https://nose.readthedocs.io/en/latest/) and
[Coverage](https://pypi.org/project/coverage/).

> TODO: Add more API tests and model/view/form tests


| Python venv | Docker |
| --- | --- |
| `$ python manage.py test --with-coverage`  | `$ docker exec hooks python manage.py test --with-coverage` |


```shell script
$ python manage.py test --with-coverage
nosetests --cover-package=hooks --cover-html --with-coverage --verbosity=1
Using selector: KqueueSelector
Creating test database for alias 'default'...
....
Name                               Stmts   Miss  Cover
------------------------------------------------------
hooks/__init__.py                      0      0   100%
hooks/admin.py                         5      5     0%
hooks/api.py                           9      0   100%
hooks/apps.py                          3      3     0%
hooks/forms.py                         6      0   100%
hooks/migrations/0001_initial.py       5      0   100%
hooks/migrations/__init__.py           0      0   100%
hooks/models.py                       11      9    18%
hooks/serializers.py                  11      0   100%
hooks/task_scheduler.py               26     15    42%
hooks/urls.py                         13      0   100%
hooks/views.py                        52     24    54%
------------------------------------------------------
TOTAL                                141     56    60%
----------------------------------------------------------------------
Ran 4 tests in 0.770s

OK
Destroying test database for alias 'default'...
```

Open interactive HTML reports at `cover/index.html`

## Manual integration tests

Run the server using [docker](docker.md) or [python venv](python-venv.md)

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) on browser

Start the test consumer on port 8888

| Python venv | Docker |
| --- | --- |
| `$ python consumer.py` | `$ docker exec -ti hooks bash` <br> `root@22aa8a5a45ca:/server# python /server/consumer.py` |

```shell script
$ cd consumer
$ python consumer.py
Starting webhook consumer on http://127.0.0.1:8888/
```

Use the already provided sample webhooks and events and trigger an event from the web app interface or from command
line using curl.

> CLI Example: `curl http://localhost:8000/trigger/create`

Verify the webhook execution in the test consumer log ...

```shell script
Received POST /audit event=create&time=2020-04-09T08%3A51%3A48.381993, Responded with 200
```

> You can also register new webhooks from the web app or using the [REST API](api.md)
>
> Use webhook URLs pointing to test consumer: `http://127.0.0.1:8888/my/test`

To test failure retry feature stop and run test consumer with a different non-OK response code like `500`

```shell script
$ cd consumer
$ python consumer.py 500
Starting webhook consumer on http://127.0.0.1:8888/
```

Trigger an event from web app and verify the same event being retried repeatedly both on the server logs and on the
consumer logs.

```shell script
$ docker logs hooks --follow | python manage.py runserver
...
...
Requesting POST http://localhost:8888/alerts {'event': 'create', 'time': '2020-04-09T08:51:48.381993'}
Requesting POST http://localhost:8888/alerts {'event': 'create', 'time': '2020-04-09T08:51:48.381993'}
Requesting POST http://localhost:8888/alerts {'event': 'create', 'time': '2020-04-09T08:51:48.381993'}
```

```shell script
$ python consumer.py 500
...
...
Received POST /alerts {"event": "create", "time": "2020-04-09T08:51:48.381993"}, Responded with 500
Received POST /alerts {"event": "create", "time": "2020-04-09T08:51:48.381993"}, Responded with 500
Received POST /alerts {"event": "create", "time": "2020-04-09T08:51:48.381993"}, Responded with 500

```

Now stop and run the consumer in default mode which will respond with the expected 200 response code and the retries
will stop.

```shell script
$ cd consumer
$ python consumer.py
Starting webhook consumer on http://127.0.0.1:8888/
Received POST /alerts {"event": "create", "time": "2020-04-09T08:51:48.381993"}, Responded with 200
```
