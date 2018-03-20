
# Dependencies:
Debian/Ubuntu hosts
(try to solve any dependencies problems with OS modules if they were appeared):

    $ sudo apt-get install python python-dev
    $ sudo apt-get install virtualenv
    $ sudo apt-get install redis-server

# Installation and running:
Install a Python Virtual Environment:

    $ virtualenv venv

Get the project sources from the Git repository:

    $ git clone ... src

Install project requirements:

    $ source venv/bin/activate
    (venv) $ pip install -r src/requirements.txt

Apply the migrations

    (venv) $ cd /path/of/project/sources/
    (venv) $ ./manage.py migrate
    (venv) $ ./manage.py collectstatic

Generate test data:

    (venv) $ ./manage.py generate_test_data

Perform tests:

    (venv) $ ./manage.py test credorg.offer.tests.CreditOrganizationTestCase

Start server:

    (venv) $ ./manage.py runserver 8888

Run CeleryD daemon:

    (venv) $ celery -A credorg worker

Open in browser link:  [http://localhost:8888/](http://localhost:8888/)

Before beginning test the API methods you have to obtain a Token key.
Go to [CreditOrganization](http://localhost:8888/admin/offer/creditorganization/)
model and select any username - it is the password too (equal).

Go to the Users section: get_token.
Press interact, enter the username and password.
Copy the token.

Go to Left Menu -> Authentication: set `token`, Scheme: `Token`, Token: `paste from clipboard`

Ok! You can test other methods with Token Authorization.



# Releases:

    # 2018-03-19 18:45 (MSK):
      - PartnerViewSchema Worksheets action: fields are described by the model ClientWorksheet;
      - generated Order.sent = None if status > 1;
      - ClientWorksheet.dob field type changed from DateTimeField to DateField;
      - Extended an API for Credit Organizations with: POST Offer;
      - Extended an API for Credit Organizations with: GET Order by PK;
      - Extended an API for Partners with: GET Worksheet by PK;
      - Added test case `test_scenario_1`.



