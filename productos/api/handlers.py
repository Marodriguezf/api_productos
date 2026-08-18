"""Manejo centralizado de errores.

Convierte cualquier excepcion en una respuesta JSON con una estructura
uniforme, de modo que el cliente siempre reciba el mismo contrato.
"""

import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler

from productos.domain.exceptions import (
    ErrorDeDominio,
    NombreDeProductoDuplicado,
    PrecioInvalido,
    ProductoNoEncontrado,
)

logger = logging.getLogger(__name__)

# Mapeo entre excepciones de dominio y codigos HTTP
CODIGOS_HTTP = {
    ProductoNoEncontrado: status.HTTP_404_NOT_FOUND,
    NombreDeProductoDuplicado: status.HTTP_409_CONFLICT,
    PrecioInvalido: status.HTTP_400_BAD_REQUEST,
}


def _cuerpo(codigo, mensaje, detalles=None):
    return {
        "exito": False,
        "error": {
            "codigo": codigo,
            "mensaje": mensaje,
            "detalles": detalles or {},
        },
    }


def manejador_de_excepciones(exc, context):
    """Handler global registrado en REST_FRAMEWORK['EXCEPTION_HANDLER']."""

    # 1. Excepciones propias del dominio
    if isinstance(exc, ErrorDeDominio):
        codigo_http = CODIGOS_HTTP.get(type(exc), status.HTTP_400_BAD_REQUEST)
        return Response(_cuerpo(exc.codigo, exc.mensaje), status=codigo_http)

    # 2. Excepciones que DRF ya sabe manejar (validacion, 404, 405, etc.)
    respuesta = exception_handler(exc, context)
    if respuesta is not None:
        detalles = respuesta.data if isinstance(respuesta.data, dict) else {}
        mensaje = "La solicitud no pudo ser procesada."
        if respuesta.status_code == status.HTTP_400_BAD_REQUEST:
            mensaje = "Los datos enviados no son validos."
        respuesta.data = _cuerpo("error_de_solicitud", mensaje, detalles)
        return respuesta

    # 3. Cualquier error no previsto -> 500 controlado
    logger.exception("Error no controlado en la API")
    return Response(
        _cuerpo("error_interno", "Ocurrio un error inesperado en el servidor."),
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
