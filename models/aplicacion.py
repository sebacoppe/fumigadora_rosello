from models.db import db

class Aplicacion(db.Model):
    __tablename__ = 'aplicacion'

    id = db.Column(db.Integer, primary_key=True)
    orden_id = db.Column(db.Integer, db.ForeignKey('orden_trabajo.id'))
    producto = db.Column(db.String(100), nullable=False)
    unidad = db.Column(db.String(20))
    cantidad_por_hectarea = db.Column(db.Float)

    #orden = db.relationship('OrdenTrabajo', backref='aplicaciones')
