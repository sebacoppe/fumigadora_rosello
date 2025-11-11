from models.db import db

class Productor(db.Model):
    __tablename__ = 'productor'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(50))
    localidad = db.Column(db.String(100))
    cuit = db.Column(db.String(20))
    
