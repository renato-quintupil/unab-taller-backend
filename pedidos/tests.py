from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.db import ProtectedError
from restaurantes.models import Restaurante, Producto
from .models import Pedido, DetallePedido


class PedidoModelTest(TestCase):
    def setUp(self):
        self.restaurante = Restaurante.objects.create(
            nombre='Restaurante Test', direccion='Dir Test'
        )
        self.producto = Producto.objects.create(
            restaurante=self.restaurante,
            nombre='Producto Test',
            precio='5000.00'
        )

    def test_estado_inicial_es_pendiente(self):
        pedido = Pedido.objects.create(cliente_nombre='Cliente Test')
        self.assertEqual(pedido.estado, 'pendiente')

    def test_producto_protegido_si_tiene_detalle(self):
        pedido = Pedido.objects.create(cliente_nombre='Cliente Test')
        DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=1,
            precio_unitario='5000.00'
        )
        with self.assertRaises(ProtectedError):
            self.producto.delete()

    def test_precio_unitario_snapshot_no_cambia(self):
        pedido = Pedido.objects.create(cliente_nombre='Cliente Test')
        detalle = DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=1,
            precio_unitario='5000.00'
        )
        self.producto.precio = '9999.00'
        self.producto.save()
        detalle.refresh_from_db()
        self.assertEqual(str(detalle.precio_unitario), '5000.00')


class PedidoAPITest(APITestCase):
    def setUp(self):
        self.restaurante = Restaurante.objects.create(
            nombre='Restaurante Test', direccion='Dir Test'
        )
        self.producto = Producto.objects.create(
            restaurante=self.restaurante,
            nombre='Producto Test',
            precio='5000.00'
        )
        self.payload_valido = {
            'cliente_nombre': 'Juan Pérez',
            'detalles': [
                {
                    'producto': self.producto.id,
                    'cantidad': 2,
                    'precio_unitario': '5000.00'
                }
            ]
        }

    def test_crear_pedido_retorna_201(self):
        url = reverse('pedido-list')
        response = self.client.post(url, self.payload_valido, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_pedido_creado_tiene_estado_pendiente(self):
        url = reverse('pedido-list')
        response = self.client.post(url, self.payload_valido, format='json')
        self.assertEqual(response.data['estado'], 'pendiente')

    def test_pedido_creado_tiene_detalles_anidados(self):
        url = reverse('pedido-list')
        response = self.client.post(url, self.payload_valido, format='json')
        self.assertEqual(len(response.data['detalles']), 1)

    def test_crear_pedido_sin_nombre_retorna_400(self):
        url = reverse('pedido-list')
        payload = {'cliente_nombre': '', 'detalles': []}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_detalle_pedido_retorna_200(self):
        pedido = Pedido.objects.create(cliente_nombre='Test')
        DetallePedido.objects.create(
            pedido=pedido,
            producto=self.producto,
            cantidad=1,
            precio_unitario='5000.00'
        )
        url = reverse('pedido-detail', args=[pedido.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('detalles', response.data)

    def test_pedido_inexistente_retorna_404(self):
        url = reverse('pedido-detail', args=[9999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
