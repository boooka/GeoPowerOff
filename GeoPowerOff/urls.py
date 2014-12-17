from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.views import static

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'GeoParse.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
                            url(r'^static/(?P<path>.*)$', 'serve'),
                            url(r"^media/(.+)", static.serve, {"document_root": settings.MEDIA_ROOT}),
                            )


