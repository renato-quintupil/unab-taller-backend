from rest_framework import viewsets, mixins
from .models import Pedido
from .serializers import PedidoSerializer


class PedidoViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
