from flask import Blueprint, render_template


facturacion_bp = Blueprint('facturacion', __name__, template_folder='../templates')

@facturacion_bp.route('/', methods=['GET'])
def listar_facturacion():
    return render_template('listar_facturacion.html')



@facturacion_bp.route('/nueva', methods=['GET', 'POST'])
def nueva_ot():
    return render_template('facturacion/nueva_ot.html')
