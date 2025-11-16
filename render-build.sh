#!/usr/bin/env bash

echo "📦 Instalando dependencias con Poetry..."
poetry install

echo "🔧 Ejecutando migraciones en render-build.sh..."
poetry run python render_migrate.py
