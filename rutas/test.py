from flask import Blueprint
from models.db import db
from datetime import date
from ordenes import OrdenTrabajo

test_bp = Blueprint('test', __name__)

@test_bp.route("/test-insert")
def test_insert():
    nueva_orden = OrdenTrabajo(
        productor_id=1,
        fecha=date.today(),
        campo="Campo Test",
        lote="Lote 1",
        observaciones="Prueba de migración",
        estado="pendiente",
        hectareas=10,
        fecha_aplicacion=None,
        fecha_inicio=None
    )
    db.session.add(nueva_orden)
    db.session.commit()
    return "✅ Orden insertada"
