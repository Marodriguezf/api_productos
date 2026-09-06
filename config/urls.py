"""Enrutamiento raiz del proyecto."""

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.views.decorators.csrf import csrf_exempt
from strawberry.django.views import GraphQLView

from productos.graphql_api.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    # Modulo de productos
    path("api/", include("productos.api.urls")),
    # Documentacion interactiva
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # GraphQL
    path(
        "graphql/",
        csrf_exempt(GraphQLView.as_view(schema=schema, graphql_ide="graphiql")),
        name="graphql",
    ),
]
