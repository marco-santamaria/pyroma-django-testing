Introduction to Django application testing with py.test
=======================================================

The blog module is a demo Django app written for PyRoma, the Python User Group of Rome.

It defines two basic models (Post, Comment) and three views.

In the test folder there are some tests that show the basic usage of

* py.test and pytest-django
* webtest for testing views
* selenium and splinter for testing client-side behaviour
* django-dynamic-fixture to create sample model instances in tests

To setup a local development environment create a virtualenv and run

    pip install -r requirements.txt

    make init-db

To run the development server

    ./manage.py runserver_plus

To launch the tests

    py.test -vv

An HTML coverage report will be generated in the folder htmlcov.
