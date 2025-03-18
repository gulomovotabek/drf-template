from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from common.swagger.generator import BothHttpAndHttpsSchemaGenerator

from project_name.settings import SWAGGER_CONFIG


def schema_view():
    return get_schema_view(
        openapi.Info(
            title=SWAGGER_CONFIG.get('title', "Nasiyah"),
            default_version="v1",
            description="Nasiyah API",
        ),
        url=SWAGGER_CONFIG['swagger_base_url'],
        public=True,
        permission_classes=(permissions.AllowAny,),
        generator_class=BothHttpAndHttpsSchemaGenerator,
    )
