from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

import api
from api.pyconfi2016 import views

YEAR = api.settings.YEAR

urlpatterns = [
    url(r'^api/admin/', admin.site.urls),

    # API
    url(r'^$', views.index),
    url(r'^api/%s/register/$' % YEAR,
        views.register),
    url(r'^api/%s/seats_left$' % YEAR,
        views.seats_left),
    url(r'^api/%s/country$' % YEAR,
        views.autocomplete_country),
]

if settings.DEBUG:
    urlpatterns += static('/', document_root='..')
