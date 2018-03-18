from rest_framework.permissions import BasePermission

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
    Allows access only to Partner users.
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

        order = Order.objects.get(id=request.data['order'])
        partner = Partner.objects.get(user=request.user)
        if order.worksheet.partner != partner:
            return False
        return True


class IsCreditOrganizationOrder(BasePermission):
    """
    Allows access only to Partner users.
    """

    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        order = Order.objects.get(id=request.data['order'])
        co = CreditOrganization.objects.get(user=request.user)
        if order.offer.credit_organization != co:
            return False
        return True
