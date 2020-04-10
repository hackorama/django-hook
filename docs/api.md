# API

Both webhooks (`api/webhooks`) and events (`api/events`) are available through RESTful API supporting CRUD operations
following standard conventions.

Please use the default browsable API console enabled at `/api` for more details.

![Browseable API Console](screenshots/api-console.png)

```shell script
$ curl  -s http://127.0.0.1:8000/api/webhooks/ | python -m json.tool
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 2,
            "name": "Alerts",
            "url": "http://localhost:8888/alerts",
            "events": [
                1,
                3
            ]
        },
        {
            "id": 3,
            "name": "Auditing",
            "url": "http://localhost:8888/audit",
            "events": [
                3
            ]
        },
        {
            "id": 1,
            "name": "Logging",
            "url": "http://localhost:8888/logging",
            "events": [
                1,
                2,
                3,
                4
            ]
        }
    ]
}
```

```shell script
$ curl  -s http://127.0.0.1:8000/api/events/ | python -m json.tool
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "create"
        },
        {
            "id": 3,
            "name": "delete"
        },
        {
            "id": 4,
            "name": "read"
        },
        {
            "id": 10,
            "name": "test"
        },
        {
            "id": 2,
            "name": "update"
        }
    ]
}

