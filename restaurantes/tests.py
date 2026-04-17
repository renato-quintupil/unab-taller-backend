from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Restaurante, Producto


class RestauranteModelTest(TestCase):
    def setUp(self):
        self.restaurante = Restaurante.objects.create(
            nombre='Test Restaurante',
            direccion='Calle Test 123'
        )

    def test_str(self):
        self.assertEqual(str(self.restaurante), 'Test Restaurante')

    def test_productos_eliminados_en_cascada(self):
        Producto.objects.create(
            restaurante=self.restaurante,
            nombre='Producto Test',
            precio='5000.00'
        )
        self.restaurante.delete()
        self.assertEqual(Producto.objects.count(), 0)


class RestauranteAPITest(APITestCase):
    def setUp(self):
        self.r1 = Restaurante.objects.create(nombre='Restaurante A', direccion='Dir A')
        self.r2 = Restaurante.objects.create(nombre='Restaurante B', direccion='Dir B')
        self.p1 = Producto.objects.create(
            restaurante=self.r1, nombre='Producto A1', precio='3000.00'
        )
        self.p2 = Producto.objects.create(
            restaurante=self.r2, nombre='Producto B1', precio='4000.00'
        )

    def test_lista_retorna_200(self):
        url = reverse('restaurante-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lista_no_incluye_productos_anidados(self):
        url = reverse('restaurante-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertNotIn('productos', item)

    def test_lista_incluye_campos_basicos(self):
        url = reverse('restaurante-list')
        response = self.client.get(url)
        item = response.data[0]
        self.assertIn('id', item)
        self.assertIn('nombre', item)
        self.assertIn('direccion', item)
        self.assertIn('imagen', item)

    def test_detalle_retorna_200_con_productos(self):
        url = reverse('restaurante-detail', args=[self.r1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('productos', response.data)

    def test_detalle_incluye_solo_productos_del_restaurante(self):
        url = reverse('restaurante-detail', args=[self.r1.id])
        response = self.client.get(url)
        ids = [p['id'] for p in response.data['productos']]
        self.assertIn(self.p1.id, ids)
        self.assertNotIn(self.p2.id, ids)

    def test_detalle_inexistente_retorna_404(self):
        url = reverse('restaurante-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_endpoint_productos_retorna_solo_del_restaurante(self):
        url = reverse('restaurante-productos', args=[self.r1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        ids = [p['id'] for p in response.data]
        self.assertIn(self.p1.id, ids)
        self.assertNotIn(self.p2.id, ids)


class ProductoAPITest(APITestCase):
    def setUp(self):
        self.r = Restaurante.objects.create(nombre='Restaurante Test', direccion='Dir')
        self.p = Producto.objects.create(
            restaurante=self.r, nombre='Producto Test', precio='2500.00'
        )

    def test_lista_productos_retorna_200(self):
        url = reverse('producto-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detalle_producto_retorna_200(self):
        url = reverse('producto-detail', args=[self.p.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_producto_inexistente_retorna_404(self):
        url = reverse('producto-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
