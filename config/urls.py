from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(settings.DJANGO_ADMIN_URL, admin.site.urls),
    url(r'^quote/', include('agent.quote.urls', namespace='quote')),
]


urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

try:
    if settings.LOCAL:
        import debug_toolbar
        urlpatterns = [
            url(r'^__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
except AttributeError:
    # don't load the debug toolbar URLs
    pass
