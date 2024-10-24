from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from database.models import Employee, Janitorial

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/funcionario/servicos', methods=['GET'])
@jwt_required()
def get_employee_services():
    funcionario_id = get_jwt_identity()


    protocolo = get_protocolo(funcionario_id)
    
    return jsonify({
        'response': 'Seus ServiÁos',
        'protocolo': protocolo
    })

def get_protocolo(funcionario_id):
    janitorials = db.session.execute(
        db.select(Janitorial).filter(Janitorial.user_id == funcionario_id)
    ).scalars()
    
    protocolo_list = [
        {
            'data': janitorial.data,
            'status': janitorial.status,
            'endereco': f"{janitorial.rua}, {janitorial.bairro}, {janitorial.area}",
            'foto_anexada': janitorial.anexo 
        } for janitorial in janitorials
    ]
    
    return protocolo_list