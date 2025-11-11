import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()

def init_app(app):
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        print("✅ Conexión con SQLAlchemy inicializada correctamente.")
    except Exception as e:
        print("❌ Error al conectar con SQLAlchemy:", e)
