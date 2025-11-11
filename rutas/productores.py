from flask import Blueprint, render_template, request, redirect, url_for
from models.productor import Productor
from models.db import db

productores_bp = Blueprint('productores', __name__)


@productores_bp.route('/productores')
def listar_productores():
    productores = Productor.query.all()
    return render_template('listar_productores.html', productores=productores)


@productores_bp.route('/productores/nuevo', methods=['GET', 'POST'])
def nuevo_productor():
    if request.method == 'POST':
        productor = Productor(
            nombre=request.form['nombre'],
            telefono=request.form['telefono'],
            localidad=request.form['localidad'],
            cuit=request.form['cuit']
        )
        db.session.add(productor)
        db.session.commit()
        return redirect(url_for('productores.listar_productores'))
    
    return render_template('nuevo_productor.html')


@productores_bp.route('/productores/resumen/<int:productor_id>')
def resumen_por_productor(productor_id):
    productor = Productor.query.get_or_404(productor_id)
    return render_template('resumen_productor.html', productor=productor)
