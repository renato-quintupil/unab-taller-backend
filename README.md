# FoodPlease — Backend API

API REST construida con Django + Django REST Framework y PostgreSQL, containerizada con Docker.

---

## Requisitos previos

- [Docker](https://www.docker.com/get-started) y Docker Compose instalados
- Git

---

## Levantar el proyecto

### 1. Clonar el repositorio

```bash
git clone <url-del-repo>
cd unab-taller-backend
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` si necesitas cambiar algún valor. Para desarrollo local los valores por defecto funcionan sin modificaciones.

### 3. Levantar los contenedores

```bash
docker compose up --build
```

Esto levanta dos servicios:
- `db` — PostgreSQL 15 en el puerto `5432`
- `api` — Django en el puerto `8000` (aplica migraciones automáticamente al iniciar)

### 4. Verificar que está corriendo

Abre en el navegador o en un cliente HTTP:

```
http://localhost:8000/api/
```

Deberías ver el explorador de la API de DRF con los endpoints disponibles.

---

## Endpoints disponibles

| Recurso       | URL                        | Métodos              |
|---------------|----------------------------|----------------------|
| Restaurantes  | `/api/restaurantes/`       | GET, POST            |
| Restaurante   | `/api/restaurantes/{id}/`  | GET, PUT, PATCH, DELETE |
| Productos     | `/api/productos/`          | GET, POST            |
| Producto      | `/api/productos/{id}/`     | GET, PUT, PATCH, DELETE |
| Pedidos       | `/api/pedidos/`            | GET, POST            |
| Pedido        | `/api/pedidos/{id}/`       | GET, PUT, PATCH, DELETE |
| Admin         | `/admin/`                  | —                    |

---

## Comandos útiles

Ejecutar en una terminal separada mientras los contenedores están corriendo:

```bash
# Crear superusuario para el admin de Django
docker compose exec api python manage.py createsuperuser

# Aplicar migraciones manualmente
docker compose exec api python manage.py migrate

# Crear nuevas migraciones tras cambiar modelos
docker compose exec api python manage.py makemigrations

# Cargar datos de prueba (omite si ya existen)
docker compose exec api python manage.py seed

# Cargar datos de prueba (borra todo y vuelve a insertar)
docker compose exec api python manage.py seed --flush

# Abrir shell de Django
docker compose exec api python manage.py shell

# Ver logs en tiempo real
docker compose logs -f api
```

---

## Detener el proyecto

```bash
# Detener contenedores (conserva los datos)
docker compose down

# Detener y eliminar volúmenes (borra la base de datos)
docker compose down -v
```

---

## Estructura del proyecto

```
unab-taller-backend/
├── config/          # Configuración de Django (settings, urls, wsgi)
├── restaurantes/    # App: restaurantes y productos
├── pedidos/         # App: pedidos
├── media/           # Archivos subidos (imágenes) — no se sube al repo
├── .env.example     # Plantilla de variables de entorno
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```
