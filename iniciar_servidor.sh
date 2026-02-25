#!/bin/bash

echo "============================================================"
echo "       NOVA STYLE - PANEL DE ADMINISTRADOR"
echo "============================================================"
echo ""

# Cambiar al directorio database
cd "$(dirname "$0")/database"

echo "[1/2] Verificando instalación de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 no está instalado"
    echo "Por favor instala Python 3 desde https://www.python.org/"
    exit 1
fi

echo "✅ Python 3 encontrado: $(python3 --version)"
echo ""

echo "[2/2] Verificando dependencias..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Instalando Flask y Flask-CORS..."
    pip3 install flask flask-cors
fi

echo "✅ Dependencias instaladas"
echo ""

echo "============================================================"
echo " 🚀 INICIANDO SERVIDOR API..."
echo "============================================================"
echo " 📍 Servidor: http://127.0.0.1:5000"
echo " 🎨 Panel Admin: ../admin/admin_mejorado.html"
echo "============================================================"
echo ""
echo " ⚠️  Presiona Ctrl+C para detener el servidor"
echo ""

python3 api_mejorada.py
