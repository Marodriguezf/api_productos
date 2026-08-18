"""Capa de acceso a datos.

Encapsula el uso del ORM para que la capa de servicios no dependa
directamente de Django QuerySets.
"""

from productos.domain.exceptions import ProductoNoEncontrado
from productos.models import Producto


class RepositorioDeProductos:
    """Operaciones de persistencia sobre la entidad Producto."""

    @staticmethod
    def listar():
        return Producto.objects.all()

    @staticmethod
    def obtener_por_id(producto_id):
        try:
            return Producto.objects.get(pk=producto_id)
        except Producto.DoesNotExist as exc:
            raise ProductoNoEncontrado() from exc

    @staticmethod
    def existe_nombre(nombre, excluir_id=None):
        consulta = Producto.objects.filter(nombre__iexact=nombre)
        if excluir_id is not None:
            consulta = consulta.exclude(pk=excluir_id)
        return consulta.exists()

    @staticmethod
    def crear(**datos):
        return Producto.objects.create(**datos)

    @staticmethod
    def actualizar(producto, **datos):
        for campo, valor in datos.items():
            setattr(producto, campo, valor)
        producto.save()
        return producto

    @staticmethod
    def eliminar(producto):
        producto.delete()
