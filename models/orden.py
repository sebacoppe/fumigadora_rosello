from models.db import db
from datetime import date

class OrdenTrabajo(db.Model):
    __tablename__ = 'orden_trabajo'  # 🔧 recomendable para claridad

    id = db.Column(db.Integer, primary_key=True)
    productor_id = db.Column(db.Integer, db.ForeignKey('productor.id'), nullable=False)
    fecha = db.Column(db.Date, default=date.today, nullable=False)
    campo = db.Column(db.String(100), nullable=False)
    lote = db.Column(db.String(100), nullable=False)
    #producto_aplicado = db.Column(db.String(100), nullable=False)
    observaciones = db.Column(db.Text)
    estado = db.Column(db.String(20), default='pendiente')  # opciones: pendiente, en_fecha, completada
    hectareas = db.Column(db.Float, nullable=False)
    fecha_aplicacion = db.Column(db.Date)
    fecha_inicio = db.Column(db.Date)
    aplicaciones = db.relationship('Aplicacion', backref='orden', lazy=True)



    productor = db.relationship('Productor', backref='ordenes')
