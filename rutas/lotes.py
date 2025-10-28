from flask import Blueprint, render_template, request, redirect
from models.db import mysql

lotes_bp = Blueprint('lotes', __name__)

# 🟢 GET /lotes/editar/<id>
@lotes_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_lote(id):
    cursor = mysql.connection.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        cursor.execute("UPDATE lotes SET nombre = %s WHERE id = %s", (nombre, id))
        mysql.connection.commit()
        return redirect('/productores')
    cursor.execute("SELECT nombre FROM lotes WHERE id = %s", (id,))
    lote = cursor.fetchone()
    return render_template('editar_lote.html', lote=lote, id=id)

# 🔴 POST /lotes/eliminar/<id>
@lotes_bp.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_lote(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM lotes WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect('/productores')
