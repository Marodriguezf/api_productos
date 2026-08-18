"""Excepciones propias del dominio de productos."""


class ErrorDeDominio(Exception):
    """Excepcion base del dominio."""

    mensaje = "Ocurrio un error en el dominio."
    codigo = "error_de_dominio"

    def __init__(self, mensaje=None):
        self.mensaje = mensaje or self.mensaje
        super().__init__(self.mensaje)


class ProductoNoEncontrado(ErrorDeDominio):
    """Se solicito un producto que no existe."""

    mensaje = "El producto solicitado no existe."
    codigo = "producto_no_encontrado"


class NombreDeProductoDuplicado(ErrorDeDominio):
    """Ya existe otro producto registrado con el mismo nombre."""

    mensaje = "Ya existe un producto registrado con ese nombre."
    codigo = "nombre_duplicado"


class PrecioInvalido(ErrorDeDominio):
    """El precio no cumple la regla de negocio."""

    mensaje = "El precio debe ser un valor mayor o igual a cero."
    codigo = "precio_invalido"
