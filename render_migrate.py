from app import app
from flask_migrate import upgrade

print("🔧 Ejecutando render_migrate.py en Render...")

with app.app_context():
    try:
        upgrade()
        print("✅ Migraciones aplicadas correctamente.")
    except Exception as e:
        print(f"❌ Error al aplicar migraciones: {e}")