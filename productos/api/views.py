"""Vistas HTTP: exponen los servicios RESTful de Producto.

Cada vista solo traduce HTTP hacia la capa de servicios y de vuelta.
"""

from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from productos.api.serializers import ProductoEntradaSerializer, ProductoSerializer
from productos.services import ServicioDeProductos


class ProductoListaCrearView(APIView):
    """Coleccion de productos: GET (listar) y POST (crear)."""

    servicio = ServicioDeProductos()

    @extend_schema(
        summary="Listar productos",
        responses=OpenApiResponse(ProductoSerializer(many=True)),
        tags=["Productos"],
    )
    def get(self, request):
        productos = self.servicio.listar()
        serializador = ProductoSerializer(productos, many=True)
        return Response(
            {"exito": True, "cantidad": len(serializador.data), "datos": serializador.data},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Crear un producto",
        request=ProductoEntradaSerializer,
        responses={201: ProductoSerializer},
        tags=["Productos"],
    )
    def post(self, request):
        entrada = ProductoEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)

        producto = self.servicio.crear(**entrada.validated_data)
        salida = ProductoSerializer(producto)
        return Response(
            {"exito": True, "datos": salida.data},
            status=status.HTTP_201_CREATED,
        )


class ProductoDetalleView(APIView):
    """Recurso individual: GET, PUT, PATCH y DELETE."""

    servicio = ServicioDeProductos()

    @extend_schema(
        summary="Consultar un producto por id",
        responses={200: ProductoSerializer},
        tags=["Productos"],
    )
    def get(self, request, producto_id):
        producto = self.servicio.obtener(producto_id)
        return Response(
            {"exito": True, "datos": ProductoSerializer(producto).data},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Actualizar un producto por completo",
        request=ProductoEntradaSerializer,
        responses={200: ProductoSerializer},
        tags=["Productos"],
    )
    def put(self, request, producto_id):
        entrada = ProductoEntradaSerializer(data=request.data)
        entrada.is_valid(raise_exception=True)

        producto = self.servicio.actualizar(producto_id, **entrada.validated_data)
        return Response(
            {"exito": True, "datos": ProductoSerializer(producto).data},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Actualizar parcialmente un producto",
        request=ProductoEntradaSerializer,
        responses={200: ProductoSerializer},
        tags=["Productos"],
    )
    def patch(self, request, producto_id):
        entrada = ProductoEntradaSerializer(data=request.data, partial=True)
        entrada.is_valid(raise_exception=True)

        producto = self.servicio.actualizar(producto_id, **entrada.validated_data)
        return Response(
            {"exito": True, "datos": ProductoSerializer(producto).data},
            status=status.HTTP_200_OK,
        )

    @extend_schema(
        summary="Eliminar un producto",
        responses={204: None},
        tags=["Productos"],
    )
    def delete(self, request, producto_id):
        self.servicio.eliminar(producto_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
