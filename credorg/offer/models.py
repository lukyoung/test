from __future__ import absolute_import, unicode_literals
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class CreditOrganization(models.Model):
    # Since there are no limits to have more than one worksheet I'm using the
    # ForeignKey in this case of table relations.
    # But if you need restrict the relations, then use OneToOneField field type.
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='organizations_list')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def orders_list(self):
        return Order.objects.filter(
            offer__credit_organization=self
        ).exclude(sent=None)


class Partner(models.Model):
    # the same condition as for CreditOrganization
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='partners_list')
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def orders_list(self):
        return Order.objects.filter(worksheet__partner=self)


class Offer(models.Model):
    OFFER_CONSUMER = 1
    OFFER_HYPOTHEC = 2
    OFFER_AUTO_LOAN = 3

    OFFER_TYPE = (
        (OFFER_CONSUMER, _('Consumer')),
        (OFFER_HYPOTHEC, _('Hypothec')),
        (OFFER_AUTO_LOAN, _('Auto loan')),
    )

    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    rotation_from = models.DateTimeField()
    rotation_to = models.DateTimeField()

    name = models.CharField(max_length=255)
    offer_type = models.PositiveSmallIntegerField(
        choices=OFFER_TYPE, default=OFFER_CONSUMER)
    score_min = models.PositiveIntegerField(default=0, blank=True)
    score_max = models.PositiveIntegerField(default=0, blank=True)
    credit_organization = models.ForeignKey(
        CreditOrganization, related_name='offers_list',
        on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ClientWorksheet(models.Model):
    partner = models.ForeignKey(
        Partner, related_name='worksheets_list', on_delete=models.CASCADE)

    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    # I decided to don't use the User.last_name and User.first_name fields
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)

    dob = models.DateTimeField()
    phone_number = models.CharField(max_length=20, unique=True)
    passport_number = models.CharField(max_length=20, unique=True)
    score = models.PositiveIntegerField(default=0, blank=True)

    class Meta:
        ordering = ('partner', 'last_name')

    def __str__(self):
        return '{} {} {}'.format(
            self.last_name.capitalize(),
            self.first_name.capitalize(),
            self.middle_name.capitalize() if self.middle_name else ''
        )

    def __int__(self):
        return self.score


class Order(models.Model):
    NEW = 0
    SENT = 1
    RECEIVED = 2
    APPROVED = 3
    DENIED = 4
    ISSUED = 5

    STATES = (
        (NEW, _('New')),
        (SENT, _('Sent')),
        (RECEIVED, _('Received')),
        (APPROVED, _('Approved')),
        (DENIED, _('Denied')),
        (ISSUED, _('Issued')),
    )

    created = models.DateTimeField(auto_now_add=True, blank=True)
    sent = models.DateTimeField(blank=True, null=True)

    worksheet = models.ForeignKey(
        ClientWorksheet, related_name='client_orders_list',
        on_delete=models.CASCADE)
    offer = models.ForeignKey(
        Offer, related_name='offer_orders_list', on_delete=models.CASCADE)

    status = models.PositiveSmallIntegerField(
        choices=STATES, default=NEW, blank=True)

    class Meta:
        ordering = ('-created',)
        unique_together = ('worksheet', 'offer')

    def __str__(self):
        return str(dict(self.STATES)[self.status])

    def send(self):
        self.sent = timezone.now()
        self.status = self.SENT
        self.save()
