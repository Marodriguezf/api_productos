"""Tipos de GraphQL.

Strawberry deriva el esquema a partir de las anotaciones de tipo de Python,
reutilizando el mismo modelo del ORM que ya usa la API REST.
"""

import decimal
import datetime

import strawberry
import strawberry_django

from productos.models import Producto


@strawberry_django.type(Producto)
class ProductoType:
    """Representacion de un Producto en el esquema GraphQL."""

    id: int
    nombre: str
    descripcion: str
    precio: decimal.Decimal
    creado_en: datetime.datetime
    actualizado_en: datetime.datetime


@strawberry.input
class ProductoEntrada:
    """Datos de entrada para crear un producto."""

    nombre: str
    precio: decimal.Decimal
    descripcion: str = ""


@strawberry.input
class ProductoActualizacion:
    """Datos de entrada para actualizar un producto.

    Todos los campos son opcionales: se actualiza solo lo que llegue.
    """

    nombre: str | None = None
    descripcion: str | None = None
    precio: decimal.Decimal | None = None


@strawberry.type
class ResultadoEliminacion:
    """Respuesta de la mutacion de eliminacion."""

    exito: bool
    mensaje: str
