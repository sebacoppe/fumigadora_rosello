from flask import Blueprint, render_template, request
from models.db import db
from models.orden import OrdenTrabajo
from models.productor import Productor
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def inicio():
    # Filtro por fechas
    desde_str = request.args.get('desde')
    hasta_str = request.args.get('hasta')

    desde = datetime.strptime(desde_str, '%Y-%m-%d').date() if desde_str else None
    hasta = datetime.strptime(hasta_str, '%Y-%m-%d').date() if hasta_str else None

    query = db.session.query(OrdenTrabajo)

    if desde and hasta:
        query = query.filter(OrdenTrabajo.fecha.between(desde, hasta))

    ordenes = query.order_by(OrdenTrabajo.fecha.desc()).all()

    # Métricas
    total_hectareas = sum(ot.hectareas for ot in ordenes if ot.hectareas)
    productores_activos = db.session.query(Productor).count()
    ot_pendientes = query.filter_by(estado='pendiente').count()
    ot_en_fecha = query.filter_by(estado='en_fecha').count()
    ot_completadas = query.filter_by(estado='completada').count()

    return render_template(
        'dashboard.html',
        ordenes=ordenes,
        total_hectareas=total_hectareas,
        productores_activos=productores_activos,
        ot_pendientes=ot_pendientes,
        ot_en_fecha=ot_en_fecha,
        ot_completadas=ot_completadas,
        desde=desde_str,
        hasta=hasta_str
    )

# 👇 ESTA FUNCIÓN VA FUERA DE inicio()
@dashboard_bp.route('/hectareas_periodo', methods=['GET'])
def hectareas_periodo():
    desde_str = request.args.get('desde')
    hasta_str = request.args.get('hasta')

    desde = datetime.strptime(desde_str, '%Y-%m-%d').date() if desde_str else None
    hasta = datetime.strptime(hasta_str, '%Y-%m-%d').date() if hasta_str else None

    query = db.session.query(OrdenTrabajo)

    if desde and hasta:
        query = query.filter(OrdenTrabajo.fecha.between(desde, hasta))

    total_hectareas = sum(ot.hectareas for ot in query.all() if ot.hectareas)

    return render_template(
        'hectareas_periodo.html',
        total_hectareas=total_hectareas,
        desde=desde_str,
        hasta=hasta_str
    )
