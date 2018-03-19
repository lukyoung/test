from __future__ import absolute_import, unicode_literals
from django.contrib.auth import authenticate
from rest_framework import viewsets, status, authentication
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import Partner, Order, CreditOrganization, Offer
from .serializers import WorksheetSerializer, OrderSerializer,\
    OfferSerializer, GetTokenCredsSerializer
from .permissions import IsPartnerUser, IsPartnerOrder, \
    IsCreditOrganizationUser, IsCreditOrganizationOrder
from .schemes import PartnerViewSchema, CreditOrganizationViewSchema, \
    AuthViewSchema
from .tasks import send_to_credorg


class AuthView(viewsets.ViewSet):
    authentication_classes = []
    permission_classes = []
    schema = AuthViewSchema()

    @list_route(['post'], url_path='GetToken', url_name='get-token')
    def get_token(self, request):
        """
        Returns the auth Token by user credentials (username and password).
        """
        serializer = GetTokenCredsSerializer(request.data)
        user = authenticate(**serializer.data)

        if not user:
            return Response(dict(error='Wrong username or password!'),
                            status=status.HTTP_401_UNAUTHORIZED)

        token = user.auth_token if hasattr(user, 'auth_token') else None
        if not token:
            return Response(dict(error='Token not defined!'),
                            status=status.HTTP_401_UNAUTHORIZED)

        return Response(dict(token=token.key))


class PartnersViewSet(viewsets.ViewSet):
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (IsPartnerUser,)
    schema = PartnerViewSchema()

    @list_route(['post', 'get'], url_path='Worksheets', url_name='worksheets')
    def worksheet(self, request):
        """
        Creates a client worksheet
        """

        partner = Partner.objects.get(user=request.user)

        if request.method == 'POST':
            data = request.data
            data.update({'partner': partner.id})

            serializer = WorksheetSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        elif request.method == 'GET':
            worksheets_list = partner.worksheets_list.select_related()

            serializer = WorksheetSerializer(worksheets_list, many=True)

            return Response(serializer.data)

    @list_route(['post', 'get'], url_path='Orders', url_name='orders')
    def order(self, request):
        """
        Creates an order
        """

        if request.method == 'POST':
            serializer = OrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        elif request.method == 'GET':
            orders = Partner.objects.get(user=request.user).orders_list()
            serializer = OrderSerializer(orders, many=True)

            return Response(serializer.data)

    @list_route(['post'], url_path='SendOrder', url_name='send-order',
                permission_classes=[IsPartnerOrder])
    def send_order(self, request):
        """
        Sends the order to the CreditOrganization
        """

        data = request.data
        order = Order.objects.get(id=data['order'])
        if order.status > Order.NEW:
            return Response(dict(error='Order already sent!'))

        # sending order to the credit organization: by email or others ways
        order.send()  # update sent field by now()
        send_to_credorg.delay(order, request.user)

        return Response(dict(status=True, order=OrderSerializer(order).data))


class CreditOrganizationViewSet(viewsets.ViewSet):
    authentication_classes = (authentication.SessionAuthentication,
                              authentication.TokenAuthentication)
    permission_classes = (IsCreditOrganizationUser,)
    schema = CreditOrganizationViewSchema()

    @list_route(['get', 'post'], url_path='Offers', url_name='offers')
    def offers(self, request):
        """
        Creates an offer
        """

        if request.method == 'POST':
            co = CreditOrganization.objects.filter(user=request.user).first()
            if not co:
                return Response(dict(error='CreditOrganization not defined!'))

            data = request.data
            data.update(dict(credit_organization=co.pk))
            serializer = OfferSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        elif request.method == 'GET':
            co = CreditOrganization.objects.filter(user=request.user).first()
            if not co:
                if request.user.is_superuser:
                    offers_list = Offer.objects.all()
                    serializer = OfferSerializer(offers_list, many=True)
                    return Response(serializer.data)

                else:
                    return Response(dict(error='Current user is not related to '
                                               'any CreditOrganization'), 403)

            offers_list = co.offers_list.select_related()
            serializer = OfferSerializer(offers_list, many=True)

            return Response(serializer.data)

    @list_route(['get'], url_path='Orders', url_name='orders')
    def orders(self, request):
        """
        Returns orders list of CreditOrganization
        """

        co = CreditOrganization.objects.filter(user=request.user).first()
        if not co:
            if request.user.is_superuser:
                orders_list = Order.objects.all()
                serializer = OrderSerializer(orders_list, many=True)
                return Response(serializer.data)

            else:
                return Response(dict(error='Current user is not related to any '
                                           'CreditOrganization'), 403)

        serializer = OrderSerializer(co.orders_list(), many=True)

        return Response(serializer.data)

    @list_route(['put'], url_path='Status', url_name='update-order-status',
                permission_classes=[IsCreditOrganizationOrder])
    def update_order_status(self, request):
        """
        Updates the status of the Order
        """

        data = request.data
        order = Order.objects.get(id=data['order'])
        order.status = data['status']
        order.save()

        return Response(dict(status=True, order=OrderSerializer(order).data))

