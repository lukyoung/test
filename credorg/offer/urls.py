from rest_framework import routers

from .views import AuthView, PartnersViewSet, CreditOrganizationViewSet


router = routers.SimpleRouter()
router.register(r'API/V1/Users', AuthView, base_name='users')
router.register(r'API/V1/Partner', PartnersViewSet, base_name='partners')
router.register(r'API/V1/CreditOrganization', CreditOrganizationViewSet,
                base_name='co')

urlpatterns = router.urls
