from flask import Blueprint, render_template, request, redirect, url_for
from models.productor import Productor
from models.orden import OrdenTrabajo
from models.db import db
from io import BytesIO
import pdfkit
from flask import send_file
from datetime import datetime
import os
import urllib.parse
from models.aplicacion import Aplicacion 



ordenes_bp = Blueprint('ordenes', __name__)


@ordenes_bp.route('/nueva_orden', methods=['GET', 'POST'])
def nueva_orden():
    if request.method == 'POST':
        fecha_str = request.form.get('fecha')
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d') if fecha_str else None

        hectareas_str = request.form.get('hectareas')
        hectareas = float(hectareas_str) if hectareas_str else 0.0

        fecha_aplicacion_str = request.form.get('fecha_aplicacion')
        fecha_aplicacion = datetime.strptime(fecha_aplicacion_str, '%Y-%m-%d') if fecha_aplicacion_str else None

        fecha_inicio_str = request.form.get('fecha_inicio')
        fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d') if fecha_inicio_str else None

        # ... continuar con la creación de la OT




        nueva_ot = OrdenTrabajo(
            productor_id=request.form['productor_id'],
            fecha=fecha,
            campo=request.form['campo'],
            lote=request.form['lote'],
            #producto_aplicado='',  # o request.form.get('producto_aplicado', ''),
            observaciones=request.form.get('observaciones', ''),
            estado='pendiente',
            hectareas=hectareas,
            fecha_aplicacion=fecha_aplicacion,
            fecha_inicio=fecha_inicio
            
            
            
            
        )
        db.session.add(nueva_ot)
        db.session.flush()  # para obtener nueva_ot.id sin hacer commit

        # Suponiendo que recibís múltiples productos desde el formulario
        productos = request.form.getlist('producto[]')
        unidades = request.form.getlist('unidad[]')
        cantidades = request.form.getlist('dosis[]')

        for producto, unidad, cantidad in zip(productos, unidades, cantidades):
            aplicacion = Aplicacion(
                orden_id=nueva_ot.id,
                producto=producto,
                unidad=unidad,
                cantidad_por_hectarea=float(cantidad)
        )
        db.session.add(aplicacion)

        db.session.commit()
        return redirect(url_for('ordenes.resumen_por_productor', productor_id=nueva_ot.productor_id))

    productor_id = request.args.get('productor_id', type=int)
    productor = Productor.query.get_or_404(productor_id)
    return render_template('nueva_orden.html', productor=productor)



@ordenes_bp.route('/resumen_productor/<int:productor_id>')
def resumen_por_productor(productor_id):
    ordenes = (
        db.session.query(OrdenTrabajo)
        .filter_by(productor_id=productor_id)
        .order_by(OrdenTrabajo.fecha.desc())
        .all()
    )

    resumen = []
    for orden in ordenes:
        resumen.append({
            'id': orden.id,
            'fecha': orden.fecha,
            'campo': orden.campo,
            'lote': orden.lote,
            'producto_aplicado': ', '.join([a.producto for a in orden.aplicaciones]),
            'observaciones': orden.observaciones
        })

    return render_template('resumen_ot_productor.html', ordenes=resumen, productor_id=productor_id)

@ordenes_bp.route('/ot/<int:ot_id>/pdf')
def exportar_ot_pdf(ot_id):
    ot = OrdenTrabajo.query.get_or_404(ot_id)
    logo_path = 'file:///' + urllib.parse.quote(os.path.abspath('static/icono.png'))
    html = render_template('ot_pdf.html', ot=ot, logo_path=logo_path)
    
    
    # 🔧 Configurar pdfkit con la ruta al ejecutable wkhtmltopdf
    config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')  # ajustá si es distinta

    # 🔧 Generar el PDF en memoria
    pdf_bytes = pdfkit.from_string(html, False, configuration=config)
    pdf_io = BytesIO(pdf_bytes)
    

    # 🔧 Enviar el PDF como archivo descargable
    return send_file(pdf_io, mimetype='application/pdf',
                        download_name=f'OT_{ot.id}_MRFUM.pdf')
    
    
@ordenes_bp.route('/ordenes')
def listar_ordenes():
        ordenes = OrdenTrabajo.query.order_by(OrdenTrabajo.fecha.desc()).all()
        return render_template('listar_ordenes.html', ordenes=ordenes)

@ordenes_bp.route('/seleccionar_productor')
def seleccionar_productor():
    productores = Productor.query.order_by(Productor.nombre).all()
    return render_template('seleccionar_productor.html', productores=productores)


@ordenes_bp.route('/ver/<int:ot_id>')
def ver_ot(ot_id):
    ot = OrdenTrabajo.query.get_or_404(ot_id)
    return render_template('ver_ot.html', ot=ot)

