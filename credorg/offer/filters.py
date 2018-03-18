from django.conf import settings
from django.contrib import admin
from django.db.models import Min, Max
from django.utils.translation import ugettext_lazy as _

from .models import Offer, CreditOrganization, Partner


class ScoresFilter(admin.SimpleListFilter):
    title = _('Scores')
    parameter_name = 'score'

    def _score_min_max_range(self, model):
        """
        Returns result of the performing of SQL: 
            select min(score), max(score)
            from offer_clientworksheet
        :param model: ClientWorksheet
        :return: {'score_min': int, 'score_max': int}
        """
        score_min_max = model.objects.all().annotate(
            score_min=Min('score'),
            score_max=Max('score')
        )
        return list(range(
            score_min_max['score_min'],
            score_min_max['score_max'] + 1,
            settings.SCORE_FILTER_SIZE
        ))

    def lookups(self, request, model_admin):
        score_min_max_range = self._score_min_max_range(model_admin)
        score_ranges = []
        score_from = score_min_max_range[0]
        for i in score_min_max_range:
            score_ranges.append(
                ('{}:{}'.format(score_from, i), '{} - {}'.format(score_from, i))
            )
            score_from = i

        return score_ranges

    def queryset(self, request, queryset):
        score_min_max_range = self._score_min_max_range(queryset.model)
        score_min = score_min_max_range[0]
        score_max = score_min_max_range[-1]
        return queryset.filter(score__gte=score_min, score__lte=score_max)


class OfferFilter(admin.SimpleListFilter):
    title = _('Offer')
    parameter_name = 'offer'

    def lookups(self, request, model_admin):
        offers = set()

        # if there is is_active field:
        # object_list = model_admin.objects.filter(
        #     is_active=True
        # ).order_by('name')

        for offer in Offer.objects.all():
            offers.add((offer.name[0].upper(), offer.name[0].upper()))
        offers = list(offers)
        offers.sort()

        return offers

    def queryset(self, request, queryset):
        raise Exception(self.value())
        v = self.value()
        if not v:
            return queryset
        try:
            return queryset.filter(offer__name__istartswith=v)
        except Exception as e:
            raise Exception(self.value())


class COUserFilter(admin.SimpleListFilter):
    title = _('User')
    parameter_name = 'credit_organization'

    def lookups(self, request, model_admin):
        users = set()
        for co in CreditOrganization.objects.select_related('user'):
            users.add((co.user_id, co.user.username.capitalize()))
        users = list(users)
        users.sort()
        return users

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(user_id=v)


class PartnerUserFilter(admin.SimpleListFilter):
    title = _('User')
    parameter_name = 'partner'

    def lookups(self, request, model_admin):
        users = set()
        for p in Partner.objects.select_related('user'):
            users.add((p.user_id, p.user.username.capitalize()))
        users = list(users)
        users.sort()
        return users

    def queryset(self, request, queryset):
        v = self.value()
        if not v:
            return queryset
        return queryset.filter(user_id=v)
