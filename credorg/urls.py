from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.views import login as login_view
from django.conf.urls import include
from rest_framework.documentation import include_docs_urls

from credorg.offer.urls import urlpatterns


urlpatterns += [
    url(r'^accounts/login/', login_view),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^', include_docs_urls(title='Credit Organization API'))
]
