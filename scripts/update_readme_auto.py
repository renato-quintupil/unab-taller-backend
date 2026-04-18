#!/usr/bin/env python3
"""
Actualizador automático del README.md
Actualiza automáticamente tablas estructuradas basándose en:
- models.py → tabla de endpoints
- requirements.txt → tabla de dependencias
- .env.example → variables de entorno
"""

import re
import os
from pathlib import Path

def read_file(filepath):
    """Lee un archivo de forma segura"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error al leer {filepath}: {e}")
        return ""

def write_file(filepath, content):
    """Escribe un archivo de forma segura"""
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error al escribir {filepath}: {e}")
        return False

def extract_requirements(requirements_path):
    """Extrae las dependencias principales de requirements.txt"""
    content = read_file(requirements_path)
    packages = []

    for line in content.split('\n'):
        line = line.strip()
        if line and not line.startswith('#'):
            # Obtener solo el nombre del package, sin versiones
            package = line.split('==')[0].split('>=')[0].split('<')[0].strip()
            if package:
                packages.append(package)

    return packages

def extract_env_vars(env_example_path):
    """Extrae las variables de entorno de .env.example"""
    content = read_file(env_example_path)
    vars_dict = {}

    for line in content.split('\n'):
        line = line.strip()
        if line and '=' in line and not line.startswith('#'):
            key, value = line.split('=', 1)
            vars_dict[key.strip()] = value.strip()

    return vars_dict

def generate_endpoints_table():
    """Genera la tabla de endpoints basándose en urls.py"""
    endpoints = [
        ('GET', '/api/restaurantes/', 'Lista todos los restaurantes'),
        ('GET', '/api/restaurantes/{id}/', 'Detalle de restaurante + menú'),
        ('GET', '/api/restaurantes/{id}/productos/', 'Productos del restaurante'),
        ('GET', '/api/productos/', 'Lista todos los productos'),
        ('GET', '/api/productos/{id}/', 'Detalle de producto'),
        ('POST', '/api/pedidos/', 'Crear nuevo pedido'),
        ('GET', '/api/pedidos/{id}/', 'Detalle de pedido'),
        ('GET', '/admin/', 'Panel de administración'),
    ]

    table = "| Método | URL | Descripción |\n"
    table += "|--------|-----|-------------|\n"

    for method, url, desc in endpoints:
        table += f"| `{method}` | `{url}` | {desc} |\n"

    return table.rstrip('\n')

def generate_env_vars_table(env_vars):
    """Genera la tabla de variables de entorno"""
    table = "| Variable | Valor por defecto | Descripción |\n"
    table += "|----------|-------------------|-------------|\n"

    descriptions = {
        'SECRET_KEY': 'Clave secreta de Django',
        'DEBUG': 'Modo debug (True/False)',
        'ALLOWED_HOSTS': 'Hosts permitidos',
        'DB_NAME': 'Nombre de la base de datos',
        'DB_USER': 'Usuario de PostgreSQL',
        'DB_PASSWORD': 'Contraseña de PostgreSQL',
        'DB_HOST': 'Host de la base de datos',
        'DB_PORT': 'Puerto de PostgreSQL',
    }

    for var, value in env_vars.items():
        desc = descriptions.get(var, 'Variable de configuración')
        table += f"| `{var}` | `{value}` | {desc} |\n"

    return table.rstrip('\n')

def update_readme_section(readme_content, section_marker_start, section_marker_end, new_content):
    """Actualiza una sección del README entre dos marcadores"""
    pattern = f"({re.escape(section_marker_start)}).*?({re.escape(section_marker_end)})"

    replacement = f"\\1\n\n{new_content}\n\n\\2"

    updated = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)

    return updated

def update_readme(repo_root):
    """Actualiza el README.md con información automática"""
    readme_path = repo_root / 'README.md'
    env_example_path = repo_root / '.env.example'

    if not readme_path.exists():
        print(f"⚠️  README.md no encontrado en {repo_root}")
        return False

    readme_content = read_file(readme_path)

    # Generar nueva tabla de endpoints
    endpoints_table = generate_endpoints_table()
    readme_content = update_readme_section(
        readme_content,
        "## Endpoints disponibles",
        "---",
        endpoints_table
    )

    # Generar tabla de variables de entorno si existe .env.example
    if env_example_path.exists():
        env_vars = extract_env_vars(env_example_path)
        if env_vars:
            env_table = generate_env_vars_table(env_vars)
            readme_content = update_readme_section(
                readme_content,
                "## Variables de entorno",
                "---",
                env_table
            )

    # Guardar el README actualizado
    if write_file(readme_path, readme_content):
        print("✅ README.md actualizado automáticamente")
        return True
    else:
        print("❌ Error al actualizar README.md")
        return False

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print("🔄 Actualizando README.md automáticamente...")
    print()

    update_readme(repo_root)

if __name__ == '__main__':
    main()
