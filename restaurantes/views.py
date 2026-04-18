from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from .models import Restaurante, Producto
from .serializers import (
    RestauranteListSerializer,
    RestauranteDetailSerializer,
    ProductoSerializer,
)


class RestauranteViewSet(viewsets.ModelViewSet):
    queryset = Restaurante.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return RestauranteDetailSerializer
        return RestauranteListSerializer

    @action(detail=True, methods=['get'], url_path='productos')
    def productos(self, request, pk=None):
        restaurante = self.get_object()
        productos = restaurante.productos.all()
        serializer = ProductoSerializer(
            productos, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ProductoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
