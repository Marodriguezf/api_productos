"""Serializadores: validan la entrada y dan forma a la salida JSON."""

from rest_framework import serializers

from productos.models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    """Representacion de salida y validacion de entrada de un Producto."""

    class Meta:
        model = Producto
        fields = ["id", "nombre", "descripcion", "precio", "creado_en", "actualizado_en"]
        read_only_fields = ["id", "creado_en", "actualizado_en"]
        # El control de nombre duplicado lo hace la capa de servicios,
        # para responder 409 Conflict en lugar de 400 Bad Request.
        extra_kwargs = {"nombre": {"validators": []}}

    def validate_nombre(self, valor):
        limpio = valor.strip()
        if len(limpio) < 3:
            raise serializers.ValidationError(
                "El nombre debe tener al menos 3 caracteres."
            )
        return limpio

    def validate_precio(self, valor):
        if valor < 0:
            raise serializers.ValidationError(
                "El precio no puede ser un valor negativo."
            )
        return valor


class ProductoEntradaSerializer(ProductoSerializer):
    """Serializador usado para POST y PUT (sin campos de solo lectura)."""

    class Meta(ProductoSerializer.Meta):
        fields = ["nombre", "descripcion", "precio"]
        read_only_fields = []
