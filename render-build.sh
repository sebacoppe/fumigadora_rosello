#!/usr/bin/env bash

echo "📦 Instalando dependencias con pip..."
pip install -r requirements.txt

echo "🔧 Ejecutando migraciones en render-build.sh..."
python render_migrate.py
