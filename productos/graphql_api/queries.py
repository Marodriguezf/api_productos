"""Consultas (queries) de GraphQL.

Reutilizan la misma capa de servicios que usa la API REST, de modo que
las reglas de negocio no se duplican entre los dos protocolos.
"""

import strawberry

from productos.domain.exceptions import ProductoNoEncontrado
from productos.graphql_api.types import ProductoType
from productos.services import ServicioDeProductos

servicio = ServicioDeProductos()


@strawberry.type
class Query:
    """Punto de entrada de todas las consultas de lectura."""

    @strawberry.field(description="Devuelve la lista completa de productos.")
    def productos(self) -> list[ProductoType]:
        return servicio.listar()

    @strawberry.field(description="Devuelve un producto por su identificador.")
    def producto(self, id: int) -> ProductoType | None:
        try:
            return servicio.obtener(id)
        except ProductoNoEncontrado:
            return None

    @strawberry.field(description="Busca productos cuyo nombre contenga el texto dado.")
    def buscar_productos(self, texto: str) -> list[ProductoType]:
        return servicio.listar().filter(nombre__icontains=texto)
