# Hooks

> What's New : Added [REST API](docs/api.md) and added [tests with code coverage](docs/tests.md)

![Main web page](docs/screenshots/webhook-app.png)

A simple [webhooks](https://en.wikipedia.org/wiki/Webhook) manager with event  triggering.

Built using [Django](https://www.djangoproject.com) web framework and [Huey](https://huey.readthedocs.io/en/latest/)
task queue.

## Quick Start

- [Deploy using Docker](docs/docker.md)
- [Run using Python venv](docs/python-venv.md)
- [REST API](docs/api.md)

> Additional [developer setup notes](docs/developer-notes.md)

## High level requirements

A Django webhooks application that:
 - Re-queues the webhooks if the server doesn't respond with a 2xx code.
 - Exposes a clean interface for registering and using the webhooks.

## Functional design

### Server application

This Django server application triggers a set of events which executes registered webhooks for each event.
The webhhok POST request execution will be submitted to a task queue which will do non-blocking execution with
retries on failure.

The application allows registering of one or more webhook url's with one or more of these events.

> This is similar to the github woobhooks registration for github events/actions.

### Client application for testing

This is a demo client application that can receive/consume a set of webhooks used for testing the server app.

> Any of the public webhooks test sites like [webhook.site](https://webhook.site) can also be used but having a local
>consumer allows us to test failure cases and retry easily.

## Server application design

### Webhook registration

Webhooks are created and linked one or more of the event/s.

### Event triggering

Events are triggered using a trigger API endpoint `trigger/<event>`

### Webhook execution

For each event trigger:
 - Lookup the webhooks for the corresponding event from database
 - Submit a POST request for each webhook with event name as the payload using a retrying task queue
 - For non-Success response or failed connection add the webhook and payload to retry queue

### Webhook task queue

Decided to use [Huey](https://huey.readthedocs.io/en/latest/) task queue which is a lightweight alternative to more
feature rich and popular task queues like Celery/RQ/Carrot.

- Can work with the built-in SQLite as the backend for demo/prototype
- Can switch to Redis as the backend easily for production
- Other task queues requires Redis or RabbitMQ even for prototype
- Has Django framework integration

## Server application data layer

The server application will use the built-in [SQLite](https://www.sqlite.org/index.html) database with data access
implemented through ORM layer using data [models](https://docs.djangoproject.com/en/3.0/topics/db/models/) and
[QuerySets](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet).

## Server application deployment

Dockerized as a simple [single image](docker.md)

## REST API

[REST API documentation](docs/api.md)

## Tests and code coverage

[Run tests with coverage reporting](docs/tests.md)

## TODO

- Dev
  - Code quality - unit tests, docstrings, type hints, pylint etc.
  - Add a common base template for all page templates
  - Add model and form constrains/validations
- Deploy (Changes for production deployment)
  - Docker compose with separate images and shared volume for database
  - Switch out SQLite with PostgreSQL/MySQL
  - Use Redis backend for Huey or switch to advanced task queue like Celery
    - Celery can provide dead-letter delivery, back-off retries etc.
  - Deploy with uWSGI and NGINX
