from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^api/2012/register/$', 'api.pyconfi2012.views.register'),
    url('^api/2012/seats_left$', 'api.pyconfi2012.views.seats_left'),
    ('^api/admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static('/', document_root='..')
