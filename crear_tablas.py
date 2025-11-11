from flask import Flask
from models.db import db, init_app

# Importar todos los modelos
from models.productor import Productor
from models.campo import Campo
from models.lote import Lote
from models.orden import Orden
from models.aplicacion import Aplicacion

app = Flask(__name__)
init_app(app)

with app.app_context():
    db.create_all()
    print("✅ Todas las tablas fueron creadas correctamente en PostgreSQL.")
