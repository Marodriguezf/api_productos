"""Rutas del modulo de productos."""

from django.urls import path

from productos.api.views import ProductoDetalleView, ProductoListaCrearView

app_name = "productos"

urlpatterns = [
    path("productos", ProductoListaCrearView.as_view(), name="lista-crear"),
    path("productos/<int:producto_id>", ProductoDetalleView.as_view(), name="detalle"),
]
