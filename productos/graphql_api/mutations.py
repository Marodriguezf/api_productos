"""Mutaciones de GraphQL: operaciones de escritura.

Igual que las consultas, delegan en la capa de servicios.
"""

import strawberry
from strawberry.types import Info

from productos.domain.exceptions import ErrorDeDominio
from productos.graphql_api.types import (
    ProductoActualizacion,
    ProductoEntrada,
    ProductoType,
    ResultadoEliminacion,
)
from productos.services import ServicioDeProductos

servicio = ServicioDeProductos()


@strawberry.type
class Mutation:
    """Punto de entrada de todas las operaciones de escritura."""

    @strawberry.mutation(description="Crea un nuevo producto.")
    def crear_producto(self, datos: ProductoEntrada) -> ProductoType:
        return servicio.crear(
            nombre=datos.nombre,
            precio=datos.precio,
            descripcion=datos.descripcion,
        )

    @strawberry.mutation(description="Actualiza los campos enviados de un producto.")
    def actualizar_producto(
        self, id: int, datos: ProductoActualizacion
    ) -> ProductoType:
        cambios = {
            campo: valor
            for campo, valor in {
                "nombre": datos.nombre,
                "descripcion": datos.descripcion,
                "precio": datos.precio,
            }.items()
            if valor is not None
        }
        return servicio.actualizar(id, **cambios)

    @strawberry.mutation(description="Elimina un producto por su identificador.")
    def eliminar_producto(self, id: int) -> ResultadoEliminacion:
        servicio.eliminar(id)
        return ResultadoEliminacion(
            exito=True, mensaje=f"El producto {id} fue eliminado."
        )
