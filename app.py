from flask import Flask,redirect,render_template
from models.db import init_app, mysql,MySQLdb
from rutas.ordenes import ordenes_bp
from rutas.productores import productores_bp
from rutas.campos import campos_bp
from rutas.lotes import lotes_bp


app = Flask(__name__)
init_app(app)
app.secret_key = 'clave_secreta'

app.register_blueprint(ordenes_bp)
app.register_blueprint(productores_bp)
app.register_blueprint(campos_bp)
app.register_blueprint(lotes_bp)


@app.route('/')
def inicio():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, nombre FROM productores")
    productores = cursor.fetchall()

    colores = ['#007bff', '#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1']  # Colores rotativos

    return render_template('inicio.html', productores=productores, colores=colores)



if __name__ == '__main__':
    app.run(debug=True)


