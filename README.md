
# Dependencies:
Debian/Ubuntu hosts:

    $ sudo apt-get install python python-dev
    $ sudo apt-get install virtualenv

# Installation and running:
Install a Python Virtual Environment:

    $ virtualenv venv

Get the project sources from the Git repository:

    $ git clone ... src

Install project requirements:

    $ source venv/bin/activate
    $ pip install -r src/requirements.txt

Apply the migrations

    $ cd /path/of/project/sources/
    $ ./manage.py migrate
    $ ./manage.py collectstatic

Generate test data:

    $ ./manage.py generate_test_data

Perform tests:

    $ ./manage.py test credorg.offer.tests.CreditOrganizationTestCase

Start server:

    $ ./manage.py runserver 8888