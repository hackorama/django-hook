# Status

- [April 3 2020](#april-3-2020)
- [April 2 2020](#april-2-2020)
- [April 1 2020](#april-1-2020)

## April 3 2020

- Added a simple webhook consumer HTTP serer for testing
- Added event trigger endpoint on the Django app for testing
- Implemented webhook execution for event triggers
- Stubbed out enqueueing of non-success response for the webhook calls

**Run the server and test consumer**

```
$  python manage.py runserver
Starting development server at http://127.0.0.1:8000/
...
```

```
$ python consumer.py
Starting webhook consumer on http://127.0.0.1:8888
...
```

**Trigger an event**

```
$ curl http://127.0.0.1:8000/trigger/create
Triggering event create ...
$
```

**Confirm registered webhooks are executed for the event**

Server finds the registered webhooks for the event and executes them

```
...
Starting development server at http://127.0.0.1:8000/
...
Submitting webhook Logging for event create ...
Making POST request at http://localhost:8888/logging with body {'event': 'create'}
Submitting webhook Alerts for event create ...
Making POST request at http://localhost:8888/alerts with body {'event': 'create'}
Submitting webhook Auditing for event create ...
Making POST request at http://localhost:8888/audit with body {'event': 'create'}
```

**Confirm the webhook calls are received on consumer side**

```
...
Starting webhook consumer on http://127.0.0.1:8888 ...
...
Received POST /audit event=create
Received POST /alerts event=create
Received POST /logging event=create
```

**Kill the consumer and trigger another event**

```
$ curl http://127.0.0.1:8000/trigger/delete
Triggering event delete ...
$
```

Verify the sever is adding the failed webhooks to retry queue

```
Submitting webhook Logging for event delete ...
Making POST request at http://localhost:8888/logging with body {'event': 'delete'}
Submitting webhook Alerts for event delete ...
Making POST request at http://localhost:8888/alerts with body {'event': 'delete'}
Submitting webhook Auditing for event delete ...
Making POST request at http://localhost:8888/audit with body {'event': 'delete'}
ERROR: Failed POST request at http://localhost:8888/logging
TODO: Add to retry queue url = http://localhost:8888/logging, event = delete
ERROR: Failed POST request at http://localhost:8888/alerts
TODO: Add to retry queue url = http://localhost:8888/alerts, event = delete
ERROR: Failed POST request at http://localhost:8888/audit
TODO: Add to retry queue url = http://localhost:8888/audit, event = delete
```


## April 2 2020

- Combining both the webhooks and caching into the same webhooks project
- Django project and application is configured and ready
- Database initialized with data models for webhooks and events
- Admin console configured for the app and models
- Admin console is used  to seed the webhooks and event objects for testing
- Added Django project configuration in [developer notes](developer-notes.md)
- Updated design, added links to status and developer notes in [README](../README.md)  

![List Webhooks](screenshots/list-webhooks.png)
![List Events](screenshots/list-events.png)
![Edit Webhooks](screenshots/edit-webhook.png)
![Add Webhooks](screenshots/add-webhook.png)

## April 1 2020

- Initial project design outline published
- Started bootstrapping the Django project

