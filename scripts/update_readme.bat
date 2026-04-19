@echo off
setlocal

set SCRIPT_DIR=%~dp0

echo Actualizando README.md...
python "%SCRIPT_DIR%update_readme_auto.py"

if %errorlevel% equ 0 (
    echo README actualizado correctamente.
) else (
    echo Error al actualizar el README.
)

endlocal
exit /b %errorlevel%
