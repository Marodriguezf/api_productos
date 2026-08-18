from django.contrib import admin

from productos.models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "creado_en")
    search_fields = ("nombre", "descripcion")
    ordering = ("id",)
