"""Capa de servicios: reglas de negocio del modulo de productos.

Las vistas no contienen logica de negocio; solo traducen HTTP <-> servicio.
"""

from decimal import Decimal

from productos.domain.exceptions import NombreDeProductoDuplicado, PrecioInvalido
from productos.repositories import RepositorioDeProductos


class ServicioDeProductos:
    """Orquesta las operaciones CRUD aplicando las reglas de negocio."""

    def __init__(self, repositorio=None):
        self.repositorio = repositorio or RepositorioDeProductos()

    # --- Consultas ---------------------------------------------------------
    def listar(self):
        return self.repositorio.listar()

    def obtener(self, producto_id):
        return self.repositorio.obtener_por_id(producto_id)

    # --- Comandos ----------------------------------------------------------
    def crear(self, nombre, precio, descripcion=""):
        self._validar_precio(precio)
        if self.repositorio.existe_nombre(nombre):
            raise NombreDeProductoDuplicado()
        return self.repositorio.crear(
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            precio=precio,
        )

    def actualizar(self, producto_id, **datos):
        producto = self.repositorio.obtener_por_id(producto_id)

        if "precio" in datos:
            self._validar_precio(datos["precio"])

        nuevo_nombre = datos.get("nombre")
        if nuevo_nombre and self.repositorio.existe_nombre(
            nuevo_nombre, excluir_id=producto_id
        ):
            raise NombreDeProductoDuplicado()

        return self.repositorio.actualizar(producto, **datos)

    def eliminar(self, producto_id):
        producto = self.repositorio.obtener_por_id(producto_id)
        self.repositorio.eliminar(producto)

    # --- Reglas privadas ---------------------------------------------------
    @staticmethod
    def _validar_precio(precio):
        if precio is None or Decimal(str(precio)) < Decimal("0"):
            raise PrecioInvalido()
