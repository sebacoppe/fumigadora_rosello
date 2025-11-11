from models.db import db

class Campo(db.Model):
    __tablename__ = 'campos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    productor_id = db.Column(db.Integer, db.ForeignKey('productores.id'))
    lotes = db.relationship('Lote', backref='campo', cascade='all, delete-orphan')