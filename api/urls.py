from django.conf.urls.defaults import patterns, url
from django.conf.urls.static import static
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url('2011/register/', 'api.pyconfi2011.views.register')
)

if settings.DEBUG:
    urlpatterns += static('/', document_root='..')
