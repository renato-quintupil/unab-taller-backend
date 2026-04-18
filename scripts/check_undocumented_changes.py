#!/usr/bin/env python3
"""
Script de auditoría diaria: Detecta cambios no documentados en el README
Se ejecuta automáticamente cada día para alertar al equipo
"""

import subprocess
from datetime import datetime, timedelta
from pathlib import Path

def get_commits_last_days(days=7):
    """Obtiene commits de los últimos N días"""
    try:
        result = subprocess.run(
            ['git', 'log', f'--since={days} days ago', '--oneline'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        return result.stdout.strip().split('\n') if result.stdout else []
    except Exception as e:
        print(f"Error al obtener commits: {e}")
        return []

def get_changed_files_in_period(days=7):
    """Obtiene archivos que cambiaron en los últimos N días"""
    try:
        result = subprocess.run(
            ['git', 'diff', f'--name-only', f'HEAD~{days*10}..HEAD'],
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        files = result.stdout.strip().split('\n') if result.stdout else []
        return [f for f in files if f]  # Filtrar vacíos
    except Exception as e:
        print(f"Error al obtener archivos modificados: {e}")
        return []

def read_readme(readme_path):
    """Lee el contenido del README"""
    try:
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error al leer README: {e}")
        return ""

def check_documentation_coverage(changed_files, readme_content):
    """Verifica qué cambios podrían no estar documentados"""
    undocumented = []

    for file in changed_files:
        # Extraer nombre del archivo para buscar en README
        filename = Path(file).name

        # Patrones a buscar en README
        search_patterns = [
            filename,  # Nombre exacto
            Path(file).stem,  # Nombre sin extensión
            file.replace('/', ' '),  # Ruta con espacios
        ]

        documented = any(pattern in readme_content for pattern in search_patterns)

        if not documented and not filename.startswith('.'):
            # Categorizar el cambio
            category = "Otro"
            if 'models.py' in file:
                category = "Modelo de datos"
            elif 'views.py' in file or 'urls.py' in file:
                category = "Endpoint/Ruta"
            elif 'requirements.txt' in file:
                category = "Dependencia"
            elif 'settings.py' in file:
                category = "Configuración"
            elif '.env' in file:
                category = "Variable de entorno"

            undocumented.append({
                'file': file,
                'category': category,
                'filename': filename
            })

    return undocumented

def generate_audit_report(commits, undocumented, readme_path):
    """Genera reporte de auditoría"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    report = f"""
================================================================================
  AUDITORÍA DIARIA — CAMBIOS SIN DOCUMENTAR
================================================================================

📅 Fecha: {timestamp}
📊 Período: Últimos 7 días
🔗 Repositorio: {Path(readme_path).parent.name}

RESUMEN:
• Total de commits: {len(commits)}
• Archivos modificados: {len(undocumented)} potencialmente sin documentar
"""

    if not undocumented:
        report += """
✅ EXCELENTE — Todos los cambios recientes parecen estar documentados en el README
"""
    else:
        report += f"""
⚠️  ALERTA — {len(undocumented)} cambio(s) que podrían no estar documentados:

"""
        # Agrupar por categoría
        by_category = {}
        for item in undocumented:
            cat = item['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item['file'])

        for category, files in sorted(by_category.items()):
            report += f"\n{category}:\n"
            for file in files:
                report += f"  • {file}\n"

        report += f"""
ACCIÓN RECOMENDADA:
1. Revisa los cambios en {Path(readme_path).parent.name}/README.md
2. Actualiza las secciones correspondientes si es necesario
3. Asegúrate de documentar nuevos endpoints, variables, o configuraciones

"""

    report += "=" * 80 + "\n"

    return report

def save_audit_report(report):
    """Guarda el reporte de auditoría"""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    audit_dir = repo_root / '.audit-reports'
    audit_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = audit_dir / f'audit_{timestamp}.txt'

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)

    print(report)
    print(f"📄 Reporte guardado en: .audit-reports/audit_{timestamp}.txt")

def main():
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    readme_path = repo_root / 'README.md'

    if not readme_path.exists():
        print(f"⚠️  README.md no encontrado en {repo_root}")
        return

    print("🔍 Ejecutando auditoría diaria...")
    print()

    # Obtener información
    commits = get_commits_last_days(7)
    changed_files = get_changed_files_in_period(7)
    readme_content = read_readme(readme_path)

    # Analizar cobertura de documentación
    undocumented = check_documentation_coverage(changed_files, readme_content)

    # Generar y guardar reporte
    report = generate_audit_report(commits, undocumented, readme_path)
    save_audit_report(report)

if __name__ == '__main__':
    main()
