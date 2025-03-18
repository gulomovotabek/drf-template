from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include

from core.swagger import schema_view


def health_check(_):
    return JsonResponse("OK", safe=False)

schema = schema_view()

urlpatterns = [
    path("", schema.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path('admin/', admin.site.urls),
    path("api/", include("apps.urls")),
    path("health-check", health_check),
]

if settings.DEBUG:
    urlpatterns += debug_toolbar_urls()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)