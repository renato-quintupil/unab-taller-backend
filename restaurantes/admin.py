from django.contrib import admin
from .models import Restaurante, Producto


@admin.register(Restaurante)
class RestauranteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'direccion']
    search_fields = ['nombre']


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'restaurante', 'precio']
    list_filter = ['restaurante']
    search_fields = ['nombre']
