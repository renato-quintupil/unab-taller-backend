from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_auth_token, name='api-token-auth'),
    path('api/', include('restaurantes.urls')),
    path('api/', include('pedidos.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
