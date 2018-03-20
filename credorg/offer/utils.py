from __future__ import absolute_import, unicode_literals
import names
import random
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi

from credorg.offer.models import CreditOrganization, Partner, Offer, \
    ClientWorksheet, Order


class FixturesGenerator(object):
    """
    This class provides an ability to generate test fixtures data
    """
    USED_NAMES = []
    CRED_ORGS_LIST = []
    PARTNERS_LIST = []
    OFFERS_LIST = []
    OFFER_TYPES = [t[0] for t in Offer.OFFER_TYPE]
    WORKSHEETS_LIST = []

    MIN_SCORE = 100
    MAX_SCORE = 0

    def clear_db(self):
        """
        Deletes all data from tables
        :return: 
        """
        Order.objects.all().delete()
        ClientWorksheet.objects.all().delete()
        Offer.objects.all().delete()
        Partner.objects.all().delete()
        CreditOrganization.objects.all().delete()

    def gen_name(self):
        """
        Returns new name
        :return: 
        """
        name = names.get_full_name()
        if name not in self.USED_NAMES:
            self.USED_NAMES.append(name)
            return name
        return self.gen_name()

    def gen_dob(self):
        year = datetime.now().year
        return timezone.make_aware(datetime(
                random.sample(range(1950, year), 1)[0],
                random.sample(range(1, 13), 1)[0],
                random.sample(range(1, 29), 1)[0]
            )).date()

    def gen_phone_number(self):
        return '79{}'.format(''.join(
            map(str, random.sample(range(0, 9), 9))
        ))

    def gen_passport_number(self):
        return ''.join(
            map(str, random.sample(list(range(0, 9))*2, 10))
        )

    def gen_score(self):
        try:
            return random.sample(
                range(self.MIN_SCORE, self.MAX_SCORE + 1), 1)[0]
        except ValueError:
            return random.randint(1, 101)

    def generate_cred_orgs(self, cred_orgs):
        """
        fill CreditOrganization table
        :param cred_orgs: 
        :return: 
        """
        cred_orgs_list = []
        for i in range(cred_orgs):
            name = self.gen_name()
            first_name, last_name = name.split()
            user = User.objects.create(
                username=name,
                last_name=last_name,
                first_name=first_name
            )
            user.set_password(name)
            user.save()

            # create authorization token
            Token.objects.create(user=user)

            # create CreditOrganization
            co = CreditOrganization.objects.create(
                name='CO {}'.format(name),
                user=user
            )

            cred_orgs_list.append(co)
        self.CRED_ORGS_LIST.extend(cred_orgs_list)

        return cred_orgs_list

    def generate_partners(self, partners):
        """
        fill Partner table
        :param partners: 
        :return: 
        """
        partners_list = []
        for i in range(partners):
            name = self.gen_name()
            user = User.objects.create(username=name)
            user.set_password(name)
            user.save()

            # create authorization token
            Token.objects.create(user=user)

            # create Partner
            p = Partner.objects.create(
                name='Parnter {}'.format(name),
                user=user
            )

            partners_list.append(p)
        self.PARTNERS_LIST.extend(partners_list)

        return partners_list

    def generate_offers(self, offers):
        """
        fill Offer table
        :param offers: 
        :return: 
        """
        offers_list = []
        for i in range(offers):
            name = self.gen_name()
            random.shuffle(self.OFFER_TYPES)
            score_min = random.randint(1, 100)
            score_max = score_min + 10
            if score_max > 100:
                score_max = 100

            # create Offer
            o = Offer.objects.create(
                rotation_from=timezone.now(),
                rotation_to=timezone.now() + timedelta(days=7),
                name=name,
                offer_type=self.OFFER_TYPES[0],
                score_min=score_min,
                score_max=score_max,
                credit_organization=random.sample(self.CRED_ORGS_LIST, 1)[0],
            )

            offers_list.append(o)

            if score_min < self.MIN_SCORE:
                self.MIN_SCORE = score_min

            if score_max > self.MAX_SCORE:
                self.MAX_SCORE = score_max
        self.OFFERS_LIST.extend(offers_list)

        return offers_list

    def generate_worksheets(self, worksheets):
        """
        fill ClientWorksheet table
        :param worksheets: 
        :return: 
        """

        for i in range(worksheets):
            name = self.gen_name()
            first_name, last_name = name.split()
            dob = self.gen_dob()
            phone_number = self.gen_phone_number()
            passport_number = self.gen_passport_number()
            random.shuffle(self.OFFER_TYPES)

            # create ClientWorksheet
            w = ClientWorksheet.objects.create(
                partner=random.sample(self.PARTNERS_LIST, 1)[0],
                last_name=last_name,
                first_name=first_name,
                dob=dob,
                phone_number=phone_number,
                passport_number=passport_number,
                score=self.gen_score(),
            )

            self.WORKSHEETS_LIST.append(w)

    def generate_orders(self, orders):
        """
        fill Order table
        :param orders: 
        :return: 
        """
        passed = []
        status_list = [s[0] for s in Order.STATES]
        for i in range(orders):
            worksheet = random.sample(self.WORKSHEETS_LIST, 1)[0]
            offer = random.sample(self.OFFERS_LIST, 1)[0]

            if (worksheet, offer) in passed:
                continue

            status = random.sample(status_list, 1)[0]
            Order.objects.create(
                sent=timezone.now() if status > 1 else None,
                worksheet=worksheet,
                offer=offer,
                status=status
            )
            passed.append((worksheet, offer))

    def generate_all(self, cred_orgs_count, partners_count, offers_count,
                     worksheets_count, orders_count):
        """
        Generates all data
        :param cred_orgs_count: 
        :param partners_count: 
        :param offers_count: 
        :param worksheets_count: 
        :param orders_count: 
        :return: 
        """
        
        self.clear_db()
        self.generate_cred_orgs(cred_orgs_count)
        self.generate_partners(partners_count)
        self.generate_offers(offers_count)
        self.generate_worksheets(worksheets_count)
        self.generate_orders(orders_count)
