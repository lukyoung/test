from django.contrib import admin
from rest_framework.authtoken.models import Token

from .models import CreditOrganization, Partner, Offer, ClientWorksheet, Order
from .filters import ScoresFilter, OfferFilter, COUserFilter, PartnerUserFilter


class OfferInline(admin.TabularInline):
    model = Offer
    readonly_fields = (
        'name', 'rotation_from', 'rotation_to', 'offer_type', 'score_min',
        'score_max', 'credit_organization'
    )
    can_delete = False


@admin.register(CreditOrganization)
class CreditOrganizationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name', 'token_repr')
    fields = ('user', 'name',)
    list_filter = (COUserFilter,)
    search_fields = ('name', 'user__username', 'user__email')
    inlines = (OfferInline,)

    def token_repr(self, obj):
        token = Token.objects.filter(user=obj.user).first()
        return token.key if token else '-'
    token_repr.short_description = 'Auth token'


class ClientWorksheetInline(admin.TabularInline):
    model = ClientWorksheet
    readonly_fields = (
        'partner', 'last_name', 'first_name', 'middle_name', 'dob',
        'phone_number', 'passport_number', 'score'
    )
    can_delete = False


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'name', 'token_repr')
    fields = ('user', 'name',)
    list_filter = (PartnerUserFilter,)
    search_fields = ('name', 'user__username', 'user__email')
    inlines = (ClientWorksheetInline,)

    def token_repr(self, obj):
        token = Token.objects.filter(user=obj.user).first()
        return token.key if token else '-'
    token_repr.short_description = 'Auth token'


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'modified', 'name', 'rotation_from',
                    'rotation_to', 'offer_type', 'score_min', 'score_max',
                    'credit_organization')
    readonly_fields = ('offer_type',)
    fields = ('name', 'rotation_from', 'rotation_to', 'offer_type', 'score_min',
              'score_max', 'credit_organization')
    # raw_id_fields = ('credit_organization',)
    list_filter = ('credit_organization', 'offer_type')
    search_fields = ('name', 'credit_organization__name',)


@admin.register(ClientWorksheet)
class ClientWorksheetAdmin(admin.ModelAdmin):
    list_display = ('pk', 'partner', 'created', 'modified', 'fio_repr', 'dob',
                    'phone_number', 'passport_number', 'score')
    readonly_fields = ('phone_number', 'passport_number',)
    fields = ('partner', 'last_name', 'first_name', 'middle_name', 'dob',
              'phone_number', 'passport_number', 'score')
    list_filter = ('partner', ScoresFilter)
    search_fields = ('name', 'credit_organization__name',)

    def fio_repr(self, obj):
        return str(obj)
    fio_repr.short_description = 'FIO'
    fio_repr.admin_order_field = 'last_name'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'sent', 'worksheet', 'offer', 'status',)
    readonly_fields = ('sent', 'worksheet', 'offer',)
    fields = ('sent', 'worksheet', 'offer', 'status')
    list_filter = ('offer', OfferFilter)
    raw_id_fields = ('offer', 'worksheet')
    search_fields = (
        'worksheet__last_name', 'worksheet__first_name',
        'worksheet__middle_name', 'worksheet__phone_number',
        'worksheet__passport_number',
        'offer__name',
        # 'offer__credit_organization__name' # this field may reduce the
        # filtering time
    )
