
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

Open in browser link:  [http://localhost:8888/](http://localhost:8888/)

Before beginning test the API methods you have to obtain a Token key.
Go to [CreditOrganization](http://localhost:8888/admin/offer/creditorganization/)
model and select any username - it is the password too (equal).

Go to the Users section: get_token.
Press interact, enter the username and password.
Copy the token.

Go to Left Menu -> Authentication: set `token`, Scheme: `Token`, Token: `paste from clipboard`

Ok! You can test other methods with Token Authorization.

