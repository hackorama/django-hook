# Tests and Coverage

Basic API tests added with code coverage enabled using [Nose](https://nose.readthedocs.io/en/latest/) and
[Coverage](https://pypi.org/project/coverage/).

> TODO: Add more API tests

> TODO: Add model/view tests

```shell script
$ python manage.py test --with-coverage
nosetests --cover-package=hooks --cover-html --with-coverage --verbosity=1
Using selector: KqueueSelector
Creating test database for alias 'default'...
..
Name                               Stmts   Miss  Cover
------------------------------------------------------
hooks/__init__.py                      0      0   100%
hooks/admin.py                         5      5     0%
hooks/api.py                           9      0   100%
hooks/apps.py                          3      3     0%
hooks/forms.py                         6      0   100%
hooks/migrations/0001_initial.py       5      0   100%
hooks/migrations/__init__.py           0      0   100%
hooks/models.py                       11     11     0%
hooks/serializers.py                  11      0   100%
hooks/urls.py                          8      0   100%
hooks/views.py                        72     51    29%
------------------------------------------------------
TOTAL                                130     70    46%
----------------------------------------------------------------------
Ran 2 tests in 0.125s

OK
Destroying test database for alias 'default'...
$
```

Open interactive HTML reports at `cover/index.html`