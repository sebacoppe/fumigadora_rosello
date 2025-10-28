from flask import Blueprint, render_template, request, redirect
from models.db import mysql
from flask import jsonify
import MySQLdb.cursors

ordenes_bp = Blueprint('ordenes', __name__)

@ordenes_bp.route('/nueva_orden', methods=['GET', 'POST'])
def nueva_orden():
    cursor = mysql.connection.cursor()

    if request.method == 'POST':
       
        # Capturar datos del formulario
        productor_id = request.form['productor_id']
        campo_id = request.form['campo_id']
        lote_id = request.form['lote_id']
        fecha = request.form['fecha']
        hectareas = request.form['hectareas']
    

        # Insertar orden
        cursor.execute("""
            INSERT INTO ordenes (productor_id, campo_id, lote_id, fecha, hectareas_estimadas)
            VALUES (%s, %s, %s, %s, %s)
        """, (productor_id, campo_id, lote_id, fecha, hectareas))
        orden_id = cursor.lastrowid

        # Insertar productos aplicados
        productos = request.form.getlist('producto[]')
        unidades = request.form.getlist('unidad[]')
        dosis = request.form.getlist('cantidad[]')

        for i in range(len(productos)):
            cursor.execute("""
                INSERT INTO aplicaciones (orden_id, producto, unidad, cantidad_por_hectarea)
                VALUES (%s, %s, %s, %s)
            """, (orden_id, productos[i], unidades[i], dosis[i]))

        mysql.connection.commit()
        return redirect(f'/resumen_productor/{productor_id}')

    # GET: Capturar parámetros desde la URL
    productor_id = request.args.get('productor_id')
    campo_id = request.args.get('campo_id')
    lote_id = request.args.get('lote_id')

    productor_nombre = campo_nombre = lote_nombre = None

    if productor_id:
        cursor.execute("SELECT nombre FROM productores WHERE id = %s", (productor_id,))
        resultado = cursor.fetchone()
        productor_nombre = resultado[0] if resultado else None

    if campo_id:
        cursor.execute("SELECT nombre FROM campos WHERE id = %s", (campo_id,))
        resultado = cursor.fetchone()
        campo_nombre = resultado[0] if resultado else None

    if lote_id:
        cursor.execute("SELECT nombre FROM lotes WHERE id = %s", (lote_id,))
        resultado = cursor.fetchone()
        lote_nombre = resultado[0] if resultado else None

    
    # Renderizar formulario vacío
    return render_template('nueva_orden.html',
        productor_id=productor_id,
        campo_id=campo_id,
        lote_id=lote_id,
        productor_nombre=productor_nombre,
        campo_nombre=campo_nombre,
        lote_nombre=lote_nombre
    )




@ordenes_bp.route('/api/campos/<int:productor_id>')
def api_campos(productor_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, nombre FROM campos WHERE productor_id = %s", (productor_id,))
    campos = cursor.fetchall()
    return jsonify(campos)


@ordenes_bp.route('/api/lotes/<int:campo_id>')
def api_lotes(campo_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT id, nombre FROM lotes WHERE campo_id = %s", (campo_id,))
    lotes = cursor.fetchall()
    return jsonify(lotes)


@ordenes_bp.route('/api/test')
def api_test():
    return "API funcionando"


@ordenes_bp.route('/resumen_productor/<int:productor_id>')
def resumen_por_productor(productor_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT o.id, o.fecha, c.nombre AS campo, l.nombre AS lote,
               GROUP_CONCAT(a.producto SEPARATOR ', ') AS productos
        FROM ordenes o
        JOIN campos c ON o.campo_id = c.id
        JOIN lotes l ON o.lote_id = l.id
        LEFT JOIN aplicaciones a ON a.orden_id = o.id
        WHERE o.productor_id = %s
        GROUP BY o.id
        ORDER BY o.fecha DESC
    """, (productor_id,))
    ordenes = cursor.fetchall()
    return render_template('resumen_ot_productor.html', ordenes=ordenes, productor_id=productor_id)


    


