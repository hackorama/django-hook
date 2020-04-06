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

## Django Huey



```shell script
$ pip install huey
```shell script

```shell script
$ vi server/settings.py
...
INSTALLED_APPS = [
     ...
    'huey.contrib.djhuey',
...
...
HUEY = {
    'huey_class': 'huey.SqliteHuey',
    'name': DATABASES['default']['NAME'],
    'immediate': False,
    # Options to pass into the consumer when running ``manage.py run_huey``
    'consumer': {
        'workers': 4,
        'worker_type': 'thread',
    },
}
...
$
```

```shell script
$ vi hooks/views.py
...
from huey.contrib.djhuey import task
...
@task()
def test_task(name):
    print('Executing %s ...' % name)
    return 'Executed task %s' % name
...
$
````

```shell script
$ python manage.py run_huey
[2020-04-04 12:31:38,265] INFO:huey.consumer:MainThread:Huey consumer started with 4 thread, PID 19278 at 2020-04-04 19:31:38.265516
[2020-04-04 12:31:38,265] INFO:huey.consumer:MainThread:Scheduler runs every 1 second(s).
[2020-04-04 12:31:38,265] INFO:huey.consumer:MainThread:Periodic tasks are enabled.
[2020-04-04 12:31:38,265] INFO:huey.consumer:MainThread:The following commands are available:
+ hooks.views.test_task
...
[2020-04-04 12:33:44,870] INFO:huey:Worker-3:Executing hooks.views.test_task: fb3dfba6-d175-44b2-aeee-c53388f742dd
Executing create ...
[2020-04-04 12:33:44,871] INFO:huey:Worker-3:hooks.views.test_task: fb3dfba6-d175-44b2-aeee-c53388f742dd executed in 0.000s
...
````


## uWSGI

```shell script
$ python -m pip install uwsgi
...
    ld: warning: ignoring file /usr/local/lib/libz.dylib, building for macOS-x86_64 but attempting to link with file built for unknown-i386
    Undefined symbols for architecture x86_64:
      "_compress", referenced from:
...
    ld: symbol(s) not found for architecture x86_64
    clang: error: linker command failed with exit code 1 (use -v to see invocation)
    *** error linking uWSGI ***
...
```

```shell script
$ brew install zlib
Updating Homebrew...
...
==> Downloading https://homebrew.bintray.com/bottles/zlib-1.2.11.catalina.bottle.tar.gz
######################################################################## 100.0%
==> Pouring zlib-1.2.11.catalina.bottle.tar.gz
==> Caveats
zlib is keg-only, which means it was not symlinked into /usr/local,
because macOS already provides this software and installing another version in
parallel can cause all kinds of trouble.

For compilers to find zlib you may need to set:
  export LDFLAGS="-L/usr/local/opt/zlib/lib"
  export CPPFLAGS="-I/usr/local/opt/zlib/include"

For pkg-config to find zlib you may need to set:
  export PKG_CONFIG_PATH="/usr/local/opt/zlib/lib/pkgconfig"

==> Summary
🍺  /usr/local/Cellar/zlib/1.2.11: 12 files, 376.4KB
```

```shell script
$ export LDFLAGS="-L/usr/local/opt/zlib/lib"
$ export CPPFLAGS="-I/usr/local/opt/zlib/include"

$ python -m pip install uwsgi
Collecting uwsgi
  Using cached https://files.pythonhosted.org/packages/e7/1e/3dcca007f974fe4eb369bf1b8629d5e342bb3055e2001b2e5340aaefae7a/uwsgi-2.0.18.tar.gz
Installing collected packages: uwsgi
  Running setup.py install for uwsgi ... done
Successfully installed uwsgi-2.0.18
```
