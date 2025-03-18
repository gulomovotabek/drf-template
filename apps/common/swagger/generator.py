from drf_yasg.generators import OpenAPISchemaGenerator

from project_name.settings import SWAGGER_CONFIG


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)

        if SWAGGER_CONFIG.get("swagger_base_url", None) and "https://" in SWAGGER_CONFIG["swagger_base_url"]:
            schema.schemes = ["https"]

        return schema
