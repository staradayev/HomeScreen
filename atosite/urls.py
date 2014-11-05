from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import autocomplete_light

autocomplete_light.autodiscover()

from care.views import UploadView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'atosite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^care/', include('care.urls', namespace="care")),
    url(r'^', include('ato.urls', namespace="ato")),
    url(r'^api/', include('api.urls', namespace="api")),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
	(r'^accounts/', include('django.contrib.auth.urls')),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
	url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
)
