from __future__ import absolute_import, unicode_literals
from rest_framework.permissions import BasePermission
from django.db.models import ObjectDoesNotExist

from .models import Partner, Order, CreditOrganization


class IsPartnerUser(BasePermission):
    """
    Allows access only to Partner users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or Partner.objects.filter(user=user).exists()


class IsCreditOrganizationUser(BasePermission):
    """
    Allows access only to CreditOrganization users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or \
            CreditOrganization.objects.filter(user=request.user).exists()


class IsPartnerOrder(BasePermission):
    """
    Allows access only to Partner users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        try:
            order = Order.objects.get(id=request.data['order'])
        except ObjectDoesNotExist:
            return False

        else:
            try:
                partner = Partner.objects.get(user=request.user)
            except ObjectDoesNotExist:
                return False

            else:
                if order.worksheet.partner_id == partner.id:
                    return True

        return False


class IsCreditOrganizationOrder(BasePermission):
    """
    Allows access only to CreditOrganization users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        try:
            order = Order.objects.get(id=request.data['order'])
        except ObjectDoesNotExist:
            return False

        else:
            try:
                co = CreditOrganization.objects.get(user=request.user)
            except ObjectDoesNotExist:
                return False

            else:
                if order.offer.credit_organization_id == co.id:
                    return True

        return False
