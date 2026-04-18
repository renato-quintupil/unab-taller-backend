# 📋 Sistema Automático de Actualizaciones README

Este documento explica cómo usar el sistema automático que sugiere actualizaciones al `README.md` cuando se realizan cambios en el proyecto.

---

## ¿Qué hace?

Después de cada `git commit`, un hook automático:

1. **Detecta** qué archivos fueron modificados (requirements.txt, Dockerfile, models.py, etc.)
2. **Analiza** qué tipo de cambio se hizo
3. **Genera** un reporte con sugerencias específicas de qué secciones del README.md podrían necesitar actualización
4. **Guarda** el reporte en `.readme-updates/` para que lo revises

---

## ✅ Primera instalación

### Opción 1: Instalación manual (si clonaste antes de esto)

Si ya tenías el repo clonado y acabas de recibir estos cambios, simplemente haz pull:

```bash
git pull origin main
```

El hook ya está en `.git/hooks/post-commit` ✅

### Opción 2: Verificar que el hook está habilitado

```bash
# En tu carpeta del backend
ls -la .git/hooks/post-commit
```

Deberías ver:
```
-rwxr-xr-x ... post-commit
```

El `x` significa que es ejecutable. Si no lo es, ejecuta:

```bash
chmod +x .git/hooks/post-commit
```

---

## 🚀 Uso

El sistema es completamente **automático**. No necesitas hacer nada especial.

### Flujo normal:

```bash
# 1. Haces cambios en tu código
git add .
git commit -m "feat: agregar nueva ruta"

# 2. Automáticamente se ejecuta el hook:
#    ↓
#    🔍 Analizando cambios para README.md...
#
#    [reporte con sugerencias]
#    📄 Reporte guardado en: .readme-updates/report_20260418_143022.txt
```

---

## 📄 Revisar reportes

Los reportes se guardan en `.readme-updates/` como archivos `.txt` con timestamp:

```
.readme-updates/
├── report_20260418_143022.txt
├── report_20260418_150045.txt
└── report_20260418_160512.txt
```

### Ejemplo de reporte:

```
================================================================================
  ANÁLISIS DE CAMBIOS — README.md SUGGESTIONS
================================================================================

📅 Fecha: 2026-04-18 14:30:22
💬 Commit: feat: agregar nueva ruta de pedidos

🔍 Se detectaron 2 cambio(s) potencial(es):

1. [Rutas/Vistas] config/urls.py
   ✏️ ACTUALIZAR: Tabla de endpoints si se agregaron rutas nuevas
   → Documentar nuevos métodos HTTP y URLs

2. [Modelos de datos] restaurantes/models.py
   ✏️ ACTUALIZAR: Sección "Endpoints disponibles" si se agregaron nuevos modelos/rutas
   → Revisar nuevos endpoints generados por los modelos

================================================================================
```

---

## 🎯 Qué tipos de cambios detecta

El sistema detecta automáticamente cambios en:

| Archivo | Sugerencia |
|---------|-----------|
| `requirements.txt` | Documentar nuevas dependencias Python |
| `Dockerfile` | Revisar cambios en imagen base |
| `docker-compose.yml` | Actualizar puertos o servicios |
| `.env.example` | Documentar nuevas variables de entorno |
| `models.py` | Agregar nuevos endpoints a la tabla |
| `urls.py` | Documentar nuevas rutas |
| `views.py` | Documentar nuevos métodos HTTP |
| `settings.py` | Revisar cambios de configuración |

---

## 💡 Recomendaciones

1. **Revisa los reportes regularmente** — especialmente después de cambios importantes
2. **Actualiza el README.md según las sugerencias** — mantén la documentación sincronizada
3. **No ignores el reporte** — es tu aliado para documentación clara
4. **Comparte con el equipo** — si ves reportes generados, comunica cambios importantes

---

## ⚙️ Configuración avanzada

### Si quieres modificar qué se detecta

Edita el archivo `scripts/check_readme_updates.py`. La función `analyze_changes()` contiene la lógica:

```python
def analyze_changes(changed_files):
    """Analiza qué tipo de cambios se hicieron"""
    for file in changed_files:
        if file.endswith('requirements.txt'):
            # ← Aquí puedes agregar nuevas condiciones
            suggestions.append({...})
```

### Si quieres desactivar el hook temporalmente

```bash
# Desactivar (renombrar)
mv .git/hooks/post-commit .git/hooks/post-commit.disabled

# Reactivar
mv .git/hooks/post-commit.disabled .git/hooks/post-commit
```

---

## 🐛 Troubleshooting

### "El hook no se ejecuta"

Verifica que sea ejecutable:
```bash
chmod +x .git/hooks/post-commit
```

### "Error: python3 no encontrado"

El hook necesita Python 3. Instálalo:
```bash
# macOS
brew install python3

# Ubuntu/Debian
sudo apt install python3
```

### "Quiero ver el reporte en la terminal"

Ya se muestra después del commit. También puedes leerlo con:
```bash
cat .readme-updates/report_*.txt
```

---

## 📞 Preguntas

¿Dudas sobre cómo funciona? Revisa el script en `scripts/check_readme_updates.py` — está bien comentado.
