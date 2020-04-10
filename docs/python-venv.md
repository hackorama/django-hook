# Python venv

Set up Python

```
$ python --version
Python 3.7.7
```

```
$ python -m venv venv
$ source venv/bin/activate
```

Install modules

```
$ pip install -r requirements.txt
```

Initialize database

```
$ cd server
$ python manage.py migrate
```

Create admin user

```
$ python manage.py createsuperuser
```

Load sample test data 

```
$ python manage.py loaddata sample-data
```

Run task queue workers

```
$ python manage.py run_huey
```

Start Django webhook server on 8000

```
$ python manage.py runserver
Starting development server at http://127.0.0.1:8000/
```

Start test consumer on port 8888

```
$ cd consumer
$ python consumer.py
Starting webhook consumer on http://127.0.0.1:8888/
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) on browser

![Main web page](screenshots/webhook-app.png)

> Register new webhooks from main app page [http://127.0.0.1:8000](http://127.0.0.1:8000) using URLs pointing to test
consumer.
>
> Example URL: `http://127.0.0.1:8888/test/one`

To test failure retry of webhooks run test consumer with a different non OK response code.

```
$ cd consumer
$ python consumer.py 501
Starting webhook consumer on http://127.0.0.1:8888/
```


> Additional [developer setup notes](docs/developer-notes.md)
