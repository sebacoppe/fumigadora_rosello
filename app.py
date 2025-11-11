from flask import Flask, render_template
from models.db import init_app, db
from models.productor import Productor
from models.orden import OrdenTrabajo
from rutas.ordenes import ordenes_bp
from rutas.productores import productores_bp
from rutas.dashboard import dashboard_bp
from rutas.facturacion import facturacion_bp
from flask_migrate import Migrate
from models.aplicacion import Aplicacion

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mi_base.db'
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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
