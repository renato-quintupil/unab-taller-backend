from rest_framework import serializers
from .models import Restaurante, Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'precio', 'imagen']


class RestauranteListSerializer(serializers.ModelSerializer):
    """Serializer ligero para el listado — sin productos anidados."""
    class Meta:
        model = Restaurante
        fields = ['id', 'nombre', 'direccion', 'imagen']


class RestauranteDetailSerializer(serializers.ModelSerializer):
    """Serializer completo para el detalle — incluye productos anidados."""
    productos = ProductoSerializer(many=True, read_only=True)

    class Meta:
        model = Restaurante
        fields = ['id', 'nombre', 'direccion', 'imagen', 'productos']
