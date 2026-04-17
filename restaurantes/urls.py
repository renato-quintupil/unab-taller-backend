from rest_framework.routers import DefaultRouter
from .views import RestauranteViewSet, ProductoViewSet

router = DefaultRouter()
router.register(r'restaurantes', RestauranteViewSet, basename='restaurante')
router.register(r'productos', ProductoViewSet, basename='producto')

urlpatterns = router.urls
