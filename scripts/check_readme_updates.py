#!/usr/bin/env python3
"""
Analizador automático de cambios para sugerir actualizaciones en README.md
Ejecutado por git hook post-commit
"""

import subprocess
import json
from datetime import datetime
from pathlib import Path

def get_last_commit_changes():
    """Obtiene los archivos modificados en el último commit"""
    try:
        result = subprocess.run(
            ['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        print(f"Error al obtener cambios: {e}")
        return []

def get_last_commit_message():
    """Obtiene el mensaje del último commit"""
    try:
        result = subprocess.run(
            ['git', 'log', '-1', '--pretty=%B'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result.stdout.strip()
    except Exception as e:
        return "No disponible"

def analyze_changes(changed_files):
    """Analiza qué tipo de cambios se hicieron y sugiere actualizaciones"""
    suggestions = []

    for file in changed_files:
        if file.endswith('requirements.txt'):
            suggestions.append({
                'archivo': file,
                'tipo': 'Dependencias',
                'sugerencia': '✏️ ACTUALIZAR: Sección "Requisitos previos" con nuevas dependencias de Python',
                'accion': 'Revisar si hay nuevas librerías importantes que documentar'
            })

        elif file.endswith('Dockerfile'):
            suggestions.append({
                'archivo': file,
                'tipo': 'Containerización',
                'sugerencia': '✏️ ACTUALIZAR: Sección "Levantar el proyecto" si cambió la imagen base o pasos',
                'accion': 'Revisar cambios en versiones de base images'
            })

        elif file.endswith('docker-compose.yml'):
            suggestions.append({
                'archivo': file,
                'tipo': 'Servicios',
                'sugerencia': '✏️ ACTUALIZAR: Sección "Endpoints disponibles" o variables de entorno si cambiaron puertos/servicios',
                'accion': 'Verificar si se agregaron o modificaron servicios'
            })

        elif file.endswith('.env.example'):
            suggestions.append({
                'archivo': file,
                'tipo': 'Variables de entorno',
                'sugerencia': '✏️ ACTUALIZAR: Tabla de "Variables de entorno" con nuevas variables',
                'accion': 'Documentar qué hace cada variable'
            })

        elif 'models.py' in file:
            suggestions.append({
                'archivo': file,
                'tipo': 'Modelos de datos',
                'sugerencia': '✏️ ACTUALIZAR: Sección "Endpoints disponibles" si se agregaron nuevos modelos/rutas',
                'accion': 'Revisar nuevos endpoints generados por los modelos'
            })

        elif 'urls.py' in file or 'views.py' in file:
            suggestions.append({
                'archivo': file,
                'tipo': 'Rutas/Vistas',
                'sugerencia': '✏️ ACTUALIZAR: Tabla de endpoints si se agregaron rutas nuevas',
                'accion': 'Documentar nuevos métodos HTTP y URLs'
            })

        elif 'settings.py' in file:
            suggestions.append({
                'archivo': file,
                'tipo': 'Configuración',
                'sugerencia': '✏️ ACTUALIZAR: Sección de configuración si hay cambios importantes',
                'accion': 'Revisar si afecta a la documentación existente'
            })

    return suggestions

def generate_report(suggestions, commit_message):
    """Genera un reporte legible"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report = f"""
================================================================================
  ANÁLISIS DE CAMBIOS — README.md SUGGESTIONS
================================================================================

📅 Fecha: {timestamp}
💬 Commit: {commit_message}

"""

    if not suggestions:
        report += "✅ No se detectaron cambios que requieran actualización del README\n"
    else:
        report += f"🔍 Se detectaron {len(suggestions)} cambio(s) potencial(es):\n\n"

        for i, sugg in enumerate(suggestions, 1):
            report += f"{i}. [{sugg['tipo']}] {sugg['archivo']}\n"
            report += f"   {sugg['sugerencia']}\n"
            report += f"   → {sugg['accion']}\n\n"

    report += "=" * 80 + "\n"

    return report

def save_report(report):
    """Guarda el reporte en un archivo"""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    reports_dir = repo_root / '.readme-updates'
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = reports_dir / f'report_{timestamp}.txt'

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(report)
    print(f"📄 Reporte guardado en: .readme-updates/report_{timestamp}.txt\n")

def main():
    changed_files = get_last_commit_changes()
    commit_message = get_last_commit_message()

    suggestions = analyze_changes(changed_files)
    report = generate_report(suggestions, commit_message)
    save_report(report)

if __name__ == '__main__':
    main()
