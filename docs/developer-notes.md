# Developer Notes

## Python

```shell script
$ python3 -m venv venv
$ source venv/bin/activate
```

```shell script
$ python --version
Python 3.7.3
```

```shell script
$ pip --version
pip 19.0.3 ...
```

## Django

Setting up a Django server.

```shell script
$ python -m pip install Django
Installing collected packages: pytz, asgiref, sqlparse, Django
Successfully installed Django-3.0.5 asgiref-3.2.7 pytz-2019.3 sqlparse-0.3.1
$
```

```shell script
$ python -m django --version
3.0.5
```

```shell script
$ django-admin startproject server
$ cd server
$ python manage.py runserver
...
System check identified no issues (0 silenced).
...
Django version 3.0.5, using settings 'server.settings'
Starting development server at http://127.0.0.1:8000/
...
$
$ python manage.py startapp hooks
...
```

Setting up the data models using built-on SQLite database.

```shell script
$ vi server/settings.py
...
TIME_ZONE = 'America/Los_Angeles'
...
$ python manage.py migrate
```

```shell script
$ vi server/settings.py
...
INSTALLED_APPS = [
    'hooks.apps.HooksConfig',
    'django.contrib.admin',
...
$
$ python manage.py makemigrations hooks
Migrations for 'hooks':
  hooks/migrations/0001_initial.py
    - Create model Webhook
    - Create model Event
$ python manage.py sqlmigrate hooks 0001
System check identified some issues:

WARNINGS:
hooks.Event.webhooks: (fields.W340) null has no effect on ManyToManyField.
BEGIN;
--
-- Create model Webhook
--
CREATE TABLE "hooks_webhook" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL, "url" varchar(200) NOT NULL);
--
-- Create model Event
--
CREATE TABLE "hooks_event" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(200) NOT NULL);
CREATE TABLE "hooks_event_webhooks" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "event_id" integer NOT NULL REFERENCES "hooks_event" ("id") DEFERRABLE INITIALLY DEFERRED, "webhook_id" integer NOT NULL REFERENCES "hooks_webhook" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE UNIQUE INDEX "hooks_event_webhooks_event_id_webhook_id_84c84057_uniq" ON "hooks_event_webhooks" ("event_id", "webhook_id");
CREATE INDEX "hooks_event_webhooks_event_id_4375d829" ON "hooks_event_webhooks" ("event_id");
CREATE INDEX "hooks_event_webhooks_webhook_id_e44a6dac" ON "hooks_event_webhooks" ("webhook_id");
COMMIT;
$ python manage.py check
System check identified no issues (0 silenced).
$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hooks, sessions
Running migrations:
  Applying hooks.0001_initial... OK
$
```

On making model changes

```shell script
$ python manage.py makemigrations
Migrations for 'hooks':
  hooks/migrations/0002_auto_20200402_1719.py
    - Remove field webhooks from event
    - Add field events to webhook
$  python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, hooks, sessions
Running migrations:
  Applying hooks.0002_auto_20200402_1719... OK
$ python manage.py check
System check identified no issues (0 silenced).
$
```

Admin user

```shell script
$ python manage.py createsuperuser
Username (leave blank to use 'hackorama'): admin
Email address: admin@hackorama.com
Password:
Password (again):
Superuser created successfully.
$
```

Run the server application

```shell script
$ python manage.py runserver
...
Django version 3.0.5, using settings 'server.settings'
Starting development server at http://127.0.0.1:8000/
...

```

