from app import app
from flask_migrate import upgrade


print("🔧 Ejecutando render_migrate.py en Render...")



with app.app_context():
    upgrade()