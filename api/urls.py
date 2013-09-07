from django.conf.urls.defaults import patterns, url, include
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

YEAR = settings.YEAR

urlpatterns = patterns(
    '',
    url('^api/%s/register/$' % YEAR, 'api.pyconfi%s.views.register' % YEAR),
    url('^api/%s/seats_left$' % YEAR, 'api.pyconfi%s.views.seats_left' % YEAR),
    ('^api/admin/', include(admin.site.urls)),

    url('^api/%s/country$' % YEAR,
        'api.pyconfi%s.views.autocomplete_country' % YEAR),
    (r'^$', 'api.pyconfi%s.views.index' % YEAR),
)

if settings.DEBUG:
    urlpatterns += static('/', document_root='..')
