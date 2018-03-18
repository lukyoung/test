from django.core.management.base import BaseCommand

from credorg.offer.utils import FixturesGenerator


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--credit_organizations_count', nargs='+', type=int)
        parser.add_argument('--partners_count', nargs='+', type=int)
        parser.add_argument('--offers_count', nargs='+', type=int)
        parser.add_argument('--worksheets_count', nargs='+', type=int)
        parser.add_argument('--orders_count', nargs='+', type=int)

    def handle(self, *args, **options):
        cred_orgs = 10
        partners = 10
        worksheets = 10
        offers = 10
        orders = 100

        if raw_input("Delete all data from database? (Y/n):").upper() == 'N':
            return

        FixturesGenerator().generate_all(
            cred_orgs, partners, offers, worksheets, orders
        )
