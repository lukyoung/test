from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import ClientWorksheet, Order, Offer


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key',)


class WorksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientWorksheet
        fields = (
            'id', 'partner', 'last_name', 'first_name', 'middle_name', 'dob',
            'phone_number', 'passport_number', 'score'
        )


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = (
            'id', 'rotation_from', 'rotation_to', 'name', 'offer_type',
            'score_min', 'score_max', 'credit_organization'
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'sent', 'worksheet', 'offer', 'status')


class GetTokenCredsSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
