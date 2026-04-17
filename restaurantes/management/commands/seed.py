"""
Management command para poblar la base de datos con datos de prueba.

Uso:
    python manage.py seed            # inserta datos (omite si ya existen)
    python manage.py seed --flush    # borra todo y vuelve a insertar
"""

from django.core.management.base import BaseCommand
from restaurantes.models import Restaurante, Producto


SEED_DATA = [
    {
        "nombre": "McDonald's",
        "direccion": "Av. Providencia 1234, Santiago",
        "productos": [
            {"nombre": "Big Mac",           "precio": 4990},
            {"nombre": "McPollo",           "precio": 4490},
            {"nombre": "Papas Fritas L",    "precio": 2490},
            {"nombre": "McFlurry Oreo",     "precio": 2990},
            {"nombre": "Coca-Cola 500ml",   "precio": 1490},
        ],
    },
    {
        "nombre": "KFC",
        "direccion": "Av. Apoquindo 5678, Las Condes",
        "productos": [
            {"nombre": "Balde Original 8 pzs",  "precio": 12990},
            {"nombre": "Combo Zinger",           "precio": 5990},
            {"nombre": "Popcorn Chicken",        "precio": 3490},
            {"nombre": "Puré con Gravy",         "precio": 1990},
            {"nombre": "Pepsi 500ml",            "precio": 1490},
        ],
    },
    {
        "nombre": "Little Caesars",
        "direccion": "Calle Huérfanos 890, Santiago Centro",
        "productos": [
            {"nombre": "Pizza Hot-N-Ready",      "precio": 6990},
            {"nombre": "Pizza Pepperoni",        "precio": 7990},
            {"nombre": "Crazy Bread (8 pzs)",    "precio": 2990},
            {"nombre": "Pizza Vegetariana",      "precio": 7490},
            {"nombre": "Coca-Cola 1.5L",         "precio": 1990},
        ],
    },
    {
        "nombre": "Domino's Pizza",
        "direccion": "Av. Irarrázaval 2345, Ñuñoa",
        "productos": [
            {"nombre": "Pizza Hawaiana M",       "precio": 8990},
            {"nombre": "Pizza BBQ Chicken M",    "precio": 9490},
            {"nombre": "Alitas BBQ (8 pzs)",     "precio": 5990},
            {"nombre": "Lava Cake",              "precio": 2490},
            {"nombre": "Sprite 500ml",           "precio": 1490},
        ],
    },
]


class Command(BaseCommand):
    help = "Pobla la base de datos con restaurantes y productos de prueba."

    def add_arguments(self, parser):
        parser.add_argument(
            "--flush",
            action="store_true",
            help="Elimina todos los restaurantes y productos antes de insertar.",
        )

    def handle(self, *args, **options):
        if options["flush"]:
            count, _ = Restaurante.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"  Eliminados {count} registros."))

        creados = 0
        omitidos = 0

        for data in SEED_DATA:
            restaurante, nuevo = Restaurante.objects.get_or_create(
                nombre=data["nombre"],
                defaults={"direccion": data["direccion"]},
            )

            if not nuevo:
                omitidos += 1
                self.stdout.write(f"  Omitido (ya existe): {restaurante.nombre}")
                continue

            creados += 1
            for p in data["productos"]:
                Producto.objects.create(
                    restaurante=restaurante,
                    nombre=p["nombre"],
                    precio=p["precio"],
                )

            self.stdout.write(
                self.style.SUCCESS(
                    f"  Creado: {restaurante.nombre} "
                    f"({len(data['productos'])} productos)"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeed completado — {creados} restaurantes creados, {omitidos} omitidos."
            )
        )
