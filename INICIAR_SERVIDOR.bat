@echo off
echo ============================================================
echo        NOVA STYLE - PANEL DE ADMINISTRADOR
echo ============================================================
echo.

REM Cambiar al directorio database
cd /d "%~dp0database"

echo [1/2] Verificando instalacion de Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python desde https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python encontrado
echo.

echo [2/2] Verificando dependencias...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Instalando Flask y Flask-CORS...
    pip install flask flask-cors
)

echo [OK] Dependencias instaladas
echo.

echo ============================================================
echo  INICIANDO SERVIDOR API...
echo ============================================================
echo  Servidor: http://127.0.0.1:5000
echo  Panel Admin: ..\admin\admin_mejorado.html
echo ============================================================
echo.
echo  Presiona Ctrl+C para detener el servidor
echo.

python api_mejorada.py

pause
