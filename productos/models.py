"""Modelo de dominio: Producto.

El ORM de Django se encarga de crear la tabla y de todas las operaciones
contra la base de datos; no se escribe SQL manual en ningun punto.
"""

from django.core.validators import MinValueValidator
from django.db import models


class Producto(models.Model):
    """Representa un producto del catalogo."""

    # id: Django lo crea automaticamente como BigAutoField (clave primaria).
    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="nombre",
        help_text="Nombre comercial del producto.",
    )
    descripcion = models.TextField(
        max_length=500,
        blank=True,
        verbose_name="descripcion",
        help_text="Descripcion breve del producto.",
    )
    precio = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="precio",
        help_text="Precio en pesos colombianos. No admite valores negativos.",
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "productos"
        ordering = ["id"]
        verbose_name = "producto"
        verbose_name_plural = "productos"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name="producto_precio_no_negativo",
            )
        ]

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
