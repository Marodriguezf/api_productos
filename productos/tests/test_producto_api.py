"""Pruebas automatizadas de los servicios RESTful de Producto."""

from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from productos.models import Producto


class ProductoAPITests(APITestCase):
    def setUp(self):
        self.url_lista = reverse("productos:lista-crear")
        self.producto = Producto.objects.create(
            nombre="Teclado mecanico",
            descripcion="Teclado con switches rojos",
            precio=Decimal("250000.00"),
        )

    def url_detalle(self, producto_id):
        return reverse("productos:detalle", args=[producto_id])

    # --- GET ---------------------------------------------------------------
    def test_listar_productos(self):
        respuesta = self.client.get(self.url_lista)
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertTrue(respuesta.data["exito"])
        self.assertEqual(respuesta.data["cantidad"], 1)

    def test_obtener_producto_existente(self):
        respuesta = self.client.get(self.url_detalle(self.producto.id))
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.assertEqual(respuesta.data["datos"]["nombre"], "Teclado mecanico")

    def test_obtener_producto_inexistente_devuelve_404(self):
        respuesta = self.client.get(self.url_detalle(9999))
        self.assertEqual(respuesta.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(respuesta.data["error"]["codigo"], "producto_no_encontrado")

    # --- POST --------------------------------------------------------------
    def test_crear_producto(self):
        datos = {
            "nombre": "Mouse inalambrico",
            "descripcion": "Mouse ergonomico bluetooth",
            "precio": "120000.00",
        }
        respuesta = self.client.post(self.url_lista, datos, format="json")
        self.assertEqual(respuesta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Producto.objects.count(), 2)

    def test_crear_producto_con_precio_negativo_falla(self):
        datos = {"nombre": "Producto malo", "descripcion": "x", "precio": "-5000"}
        respuesta = self.client.post(self.url_lista, datos, format="json")
        self.assertEqual(respuesta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(respuesta.data["exito"])

    def test_crear_producto_con_nombre_duplicado_falla(self):
        datos = {
            "nombre": "Teclado mecanico",
            "descripcion": "Duplicado",
            "precio": "99000",
        }
        respuesta = self.client.post(self.url_lista, datos, format="json")
        self.assertEqual(respuesta.status_code, status.HTTP_409_CONFLICT)
        self.assertEqual(respuesta.data["error"]["codigo"], "nombre_duplicado")

    # --- PUT ---------------------------------------------------------------
    def test_actualizar_producto(self):
        datos = {
            "nombre": "Teclado mecanico RGB",
            "descripcion": "Version actualizada",
            "precio": "310000.00",
        }
        respuesta = self.client.put(
            self.url_detalle(self.producto.id), datos, format="json"
        )
        self.assertEqual(respuesta.status_code, status.HTTP_200_OK)
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Teclado mecanico RGB")
        self.assertEqual(self.producto.precio, Decimal("310000.00"))

    def test_actualizar_producto_inexistente_devuelve_404(self):
        datos = {"nombre": "Cualquiera", "descripcion": "x", "precio": "1000"}
        respuesta = self.client.put(self.url_detalle(9999), datos, format="json")
        self.assertEqual(respuesta.status_code, status.HTTP_404_NOT_FOUND)

    # --- DELETE ------------------------------------------------------------
    def test_eliminar_producto(self):
        respuesta = self.client.delete(self.url_detalle(self.producto.id))
        self.assertEqual(respuesta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Producto.objects.count(), 0)

    def test_eliminar_producto_inexistente_devuelve_404(self):
        respuesta = self.client.delete(self.url_detalle(9999))
        self.assertEqual(respuesta.status_code, status.HTTP_404_NOT_FOUND)
