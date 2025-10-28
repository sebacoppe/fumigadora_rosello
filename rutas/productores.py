from flask import Blueprint, render_template,request,redirect,url_for
from models.db import mysql,MySQLdb

productores_bp = Blueprint('productores', __name__)


@productores_bp.route('/productores')
def listar_productores():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # Productores
    cursor.execute("SELECT id, nombre, cuit, localidad FROM productores")
    productores = cursor.fetchall()

    # Campos
    cursor.execute("SELECT id, nombre, productor_id FROM campos")
    campos = cursor.fetchall()

    # Lotes
    cursor.execute("SELECT id, nombre, campo_id FROM lotes")
    lotes = cursor.fetchall()

    return render_template('listar_productores.html', productores=productores, campos=campos, lotes=lotes)




@productores_bp.route('/productores/nuevo', methods=['GET', 'POST'])
def nuevo_productor():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        localidad = request.form['localidad']
        cuit = request.form['cuit']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO productores (nombre, telefono, localidad, cuit) VALUES (%s, %s, %s, %s)",
                       (nombre, telefono, localidad, cuit))
        mysql.connection.commit()
        return redirect(url_for('productores.listar_productores'))
    return render_template('nuevo_productor.html')
