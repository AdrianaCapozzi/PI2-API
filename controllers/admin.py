from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from database import db
from database.models import Funcionario

admin_bp = Blueprint('admin_bp', __name__)


@admin_bp.route('/funcionarios/', methods=['POST'])
@jwt_required()
def create_employee():
    request_data = request.get_json()
    

    required_fields = ['nome', 'email', 'telefone', 'setor', 'cargo', 'interno']
    missing_fields = [field for field in required_fields if field not in request_data]
    
    if missing_fields:
        return jsonify({'error': f'Campos obrigatÛrios faltando: {", ".join(missing_fields)}'}), 400
    
    try:
        funcionario = Funcionario(
            nome=request_data['nome'],
            email=request_data['email'],
            telefone=request_data['telefone'],
            setor=request_data['setor'],
            cargo=request_data['cargo'],
            interno=request_data['interno'],  
            empresa_terceirizada=request_data.get('empresa_terceirizada')  # campo opcional
        )
        db.session.add(funcionario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao cadastrar funcion·rio', 'details': str(e)}), 500

    return jsonify({'response': 'Funcion·rio cadastrado com sucesso!'}), 201


@admin_bp.route('/funcionarios/', methods=['GET'])
@jwt_required()
def get_all_employees():
    try:
        funcionarios = Funcionario.query.all()
        funcionarios_list = [
            {
                'id': func.id,
                'nome': func.nome,
                'email': func.email,
                'telefone': func.telefone,
                'setor': func.setor,
                'cargo': func.cargo,
                'interno': func.interno,
                'empresa_terceirizada': func.empresa_terceirizada
            }
            for func in funcionarios
        ]
        return jsonify(funcionarios_list), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar funcion·rios', 'details': str(e)}), 500


@admin_bp.route('/funcionarios/<int:id>', methods=['GET'])
@jwt_required()
def get_employee(id):
    try:
        funcionario = Funcionario.query.get_or_404(id)
        return jsonify({
            'id': funcionario.id,
            'nome': funcionario.nome,
            'email': funcionario.email,
            'telefone': funcionario.telefone,
            'setor': funcionario.setor,
            'cargo': funcionario.cargo,
            'interno': funcionario.interno,
            'empresa_terceirizada': funcionario.empresa_terceirizada
        }), 200
    except Exception as e:
        return jsonify({'error': 'Erro ao buscar funcion·rio', 'details': str(e)}), 500


@admin_bp.route('/funcionarios/<int:id>', methods=['PUT'])
@jwt_required()
def update_employee(id):
    funcionario = Funcionario.query.get_or_404(id)
    request_data = request.get_json()
    
    try:
        funcionario.nome = request_data.get('nome', funcionario.nome)
        funcionario.email = request_data.get('email', funcionario.email)
        funcionario.telefone = request_data.get('telefone', funcionario.telefone)
        funcionario.setor = request_data.get('setor', funcionario.setor)
        funcionario.cargo = request_data.get('cargo', funcionario.cargo)
        funcionario.interno = request_data.get('interno', funcionario.interno)
        funcionario.empresa_terceirizada = request_data.get('empresa_terceirizada', funcionario.empresa_terceirizada)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao atualizar funcion·rio', 'details': str(e)}), 500
    
    return jsonify({'response': 'Funcion·rio atualizado com sucesso!'}), 200


@admin_bp.route('/funcionarios/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_employee(id):
    funcionario = Funcionario.query.get_or_404(id)
    
    try:
        db.session.delete(funcionario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erro ao excluir funcion·rio', 'details': str(e)}), 500
    
    return jsonify({'response': 'Funcion·rio excluÌdo com sucesso!'}), 200
