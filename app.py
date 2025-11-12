from flask import Flask, render_template
from models.db import init_app, db
from models.productor import Productor
from models.orden import OrdenTrabajo
from rutas.ordenes import ordenes_bp
from rutas.productores import productores_bp
from rutas.dashboard import dashboard_bp
from rutas.facturacion import facturacion_bp
from flask_migrate import Migrate,upgrade
from models.aplicacion import Aplicacion
import os 

app = Flask(__name__)
import os
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mi_base.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base.db'
app.secret_key = 'clave_secreta'

init_app(app)
migrate = Migrate(app, db)

# Registrar blueprints
app.register_blueprint(ordenes_bp, url_prefix='/ordenes')
app.register_blueprint(productores_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(facturacion_bp, url_prefix='/facturacion')

@app.route('/')
def inicio():
    productores = Productor.query.all()
    colores = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1']
    return render_template('inicio.html', productores=productores, colores=colores)



with app.app_context():
    upgrade()

if __name__ == '__main__':
    app.run(debug=True)
    
    
    