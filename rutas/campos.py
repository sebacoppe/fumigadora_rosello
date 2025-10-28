from flask import Blueprint, render_template, request, redirect
from models.db import mysql

campos_bp = Blueprint('campos', __name__)

# 🟢 GET /campos/editar/<id>
@campos_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_campo(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        cursor.execute("UPDATE campos SET nombre = %s WHERE id = %s", (nombre, id))
        mysql.connection.commit()
        return redirect('/productores')
    cursor.execute("SELECT nombre FROM campos WHERE id = %s", (id,))
    campo = cursor.fetchone()
    return render_template('editar_campo.html', campo=campo, id=id)

# 🔴 POST /campos/eliminar/<id>
@campos_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_campo(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM campos WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect('/productores')
