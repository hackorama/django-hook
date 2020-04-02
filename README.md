# Django Hook

A simple [webhooks](https://en.wikipedia.org/wiki/Webhook) demo application using
[Django](https://www.djangoproject.com).

## High level requirement

A Django webhooks application that:
 - Re-queues the webhooks if the server doesn't respond with a 2xx code.
 - Exposes a clean interface for registering and using the webhooks.

## Functional design

### Server application

This demo server application triggers a set of pre-defined events. These events can be triggered on demand using
a REST API and/or randomly triggered periodically in the main application loop.

The demo application allows registering of one or more webhook url's with one or more of these pre-defined events
using REST API.

> This is similar to the github woobhooks registration for github events/actions.

### Client application for testing

This is a demo client application that can receive/consume a set of webhooks used for testing the server app.
This client will have webhok endpoint than can respond with custom response code range to test the re-queuing
on server app.

> Any of the public webhooks test sites like [webhook.site](https://webhook.site) can also be used for normal testing
> without the re-queuing scenario.

> Client app tests could be replaced/replicated with using
>[unittest.mock](https://docs.python.org/3/library/unittest.mock.html)

## Server design

### Webhooks registration

> TODO: Details of registering webhooks linked to application events

### Event triggering

> TODO: Details of the pre-defined events and how to trigger them for testing registered webhooks

