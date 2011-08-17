from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url('^api/2011/register/', 'api.pyconfi2011.views.register'),
    ('^api/admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static('/', document_root='..')
