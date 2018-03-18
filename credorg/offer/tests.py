import names
from django.test import TestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from .utils import FixturesGenerator
from .models import User, Order


class CreditOrganizationTestCase(TestCase):
    def setUp(self):
        self.fg = FixturesGenerator()
        self.fg.generate_all(3, 3, 10, 10, 100)

    def test_get_token_no_token_error(self):
        """
        Checks an exception when token not defined
        :return: 
        """
        name = names.get_full_name()
        user = User.objects.create(username=name)
        user.set_password(name)
        user.save()

        client = APIClient()
        res = client.post(
            '/API/V1/Users/GetToken/',
            dict(username=name, password=name),
            format='json'
        )
        self.assertIsInstance(res.data, dict)
        self.assertIsNotNone(res.data.get('error'))
        self.assertEqual(res.data['error'], 'Token not defined!')

    def test_get_token_success(self):
        """
        Checks the token
        :return: 
        """
        name = names.get_full_name()
        user = User.objects.create(username=name)
        user.set_password(name)
        user.save()
        Token.objects.create(user=user)

        client = APIClient()
        res = client.post(
            '/API/V1/Users/GetToken/',
            dict(username=name, password=name),
            format='json'
        )
        self.assertIsInstance(res.data, dict)
        self.assertIsNotNone(res.data.get('token'))

    def test_create_worksheet_by_parnter_unauthorized(self):
        """
        Checks unauthorized request: not Token in headers 
        :return: 
        """
        client = APIClient()
        res = client.post('/API/V1/Partner/Worksheets/', {}, format='json')
        self.assertEqual(res.status_code, 403)

    def test_create_worksheet_by_partner_with_wrong_data(self):
        partner = self.fg.PARTNERS_LIST[0]
        name = self.fg.gen_name()
        first_name, last_name = name.split()
        score = self.fg.gen_score()
        token = Token.objects.get(user=partner.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post(
            '/API/V1/Partner/Worksheets/',
            dict(
                last_name_WRONG_REQUIRED_FIELD_EXAMPLE=last_name,
                first_name=first_name,
                dob=self.fg.gen_dob(),
                phone_number=self.fg.gen_phone_number(),
                passport_number=self.fg.gen_passport_number(),
                score=score
            ),
            format='json'
        )
        self.assertEqual(res.status_code, 400)
        self.assertIsInstance(res.data, dict)
        self.assertIsNotNone(res.data.get('last_name'))

    def test_create_worksheet_by_partner(self):
        partner = self.fg.PARTNERS_LIST[0]
        token = Token.objects.get(user=partner.user)

        name = self.fg.gen_name()
        first_name, last_name = name.split()
        score = self.fg.gen_score()
        phone_number = self.fg.gen_phone_number()
        passport_number = self.fg.gen_passport_number()

        data = dict(
            last_name=last_name,
            first_name=first_name,
            dob=self.fg.gen_dob(),
            phone_number=phone_number,
            passport_number=passport_number,
            score=score
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post('/API/V1/Partner/Worksheets/', data, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, dict)
        self.assertIsNotNone(res.data.get('partner'))
        self.assertEqual(res.data['partner'], partner.id)
        self.assertEqual(res.data['phone_number'], phone_number)
        self.assertEqual(res.data['passport_number'], passport_number)
        self.assertEqual(res.data['score'], score)

    def test_create_order(self):
        partner = self.fg.PARTNERS_LIST[0]
        offer = self.fg.OFFERS_LIST[0]
        token = Token.objects.get(user=partner.user)

        # create Worksheet

        name = self.fg.gen_name()
        first_name, last_name = name.split()
        score = self.fg.gen_score()
        phone_number = self.fg.gen_phone_number()
        passport_number = self.fg.gen_passport_number()

        data = dict(
            last_name=last_name,
            first_name=first_name,
            dob=self.fg.gen_dob(),
            phone_number=phone_number,
            passport_number=passport_number,
            score=score
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post('/API/V1/Partner/Worksheets/', data, format='json')

        # create Order

        worksheet = res.data['id']
        data = dict(worksheet=worksheet, offer=offer.id)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post('/API/V1/Partner/Orders/', data, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, dict)
        self.assertEqual(res.data.get('status'), 0)
        self.assertEqual(res.data['worksheet'], worksheet)
        self.assertEqual(res.data['offer'], offer.id)

    def test_send_order(self):
        partner = self.fg.PARTNERS_LIST[0]
        offer = self.fg.OFFERS_LIST[0]
        token = Token.objects.get(user=partner.user)

        # create Worksheet

        name = self.fg.gen_name()
        first_name, last_name = name.split()
        score = self.fg.gen_score()
        phone_number = self.fg.gen_phone_number()
        passport_number = self.fg.gen_passport_number()

        data = dict(
            last_name=last_name,
            first_name=first_name,
            dob=self.fg.gen_dob(),
            phone_number=phone_number,
            passport_number=passport_number,
            score=score
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post('/API/V1/Partner/Worksheets/', data, format='json')

        # create Order

        worksheet = res.data['id']
        data = dict(worksheet=worksheet, offer=offer.id)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post('/API/V1/Partner/Orders/', data, format='json')

        order = res.data['id']

        # send created Order to the CreditOrganization

        data = dict(order=order, offer=offer.id)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.post('/API/V1/Partner/SendOrder/', data, format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, dict)
        self.assertTrue(res.data['status'])

    def test_get_partner_orders(self):
        partner = self.fg.PARTNERS_LIST[0]
        token = Token.objects.get(user=partner.user)

        # send created Order to the CreditOrganization

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.get('/API/V1/Partner/Orders/', format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)
        self.assertTrue(len(res.data) > 0)

    def test_get_credit_organization_orders(self):
        co = self.fg.CRED_ORGS_LIST[0]
        token = Token.objects.get(user=co.user)

        # send created Order to the CreditOrganization

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.get('/API/V1/CreditOrganization/Orders/', format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)

    def test_get_worksheets(self):
        partner = self.fg.PARTNERS_LIST[0]
        token = Token.objects.get(user=partner.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.get('/API/V1/Partner/Worksheets/', format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)
        self.assertTrue(len(res.data) > 0)

    def test_get_offers(self):
        co = self.fg.CRED_ORGS_LIST[0]
        token = Token.objects.get(user=co.user)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.get('/API/V1/CreditOrganization/Offers/', format='json')

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res.data, list)
        self.assertTrue(len(res.data) > 0)

    def test_update_alien_order_status(self):
        co = self.fg.CRED_ORGS_LIST[0]
        order = Order.objects.exclude(offer__credit_organization=co).first()
        token = Token.objects.get(user=co.user)

        data = dict(
            order=order.id,
            status=Order.RECEIVED
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.put('/API/V1/CreditOrganization/Status/', data,
                         format='json')

        self.assertEqual(res.status_code, 403)

    def test_update_own_order_status(self):
        co = self.fg.CRED_ORGS_LIST[0]
        order = Order.objects.filter(offer__credit_organization=co).first()
        token = Token.objects.get(user=co.user)

        data = dict(
            order=order.id,
            status=Order.RECEIVED
        )

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        res = client.put('/API/V1/CreditOrganization/Status/', data,
                          format='json')

        self.assertEqual(res.status_code, 200)

