
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
import os
from src.database.querys import UserQuerys
from flask_login import login_required
from src.settings import TestingConfig

admin_app = Blueprint("admin_app", __name__, url_prefix="/home/")

def public_endpoint(function):
    """Decorator for public routes"""
    function.is_public = True
    return function

@public_endpoint
@admin_app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "Nenhum arquivo encontrado."}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "Nome do arquivo vazio."}), 400

    try:
        # Salvar o arquivo no caminho especificado
        file_path = os.path.join(TestingConfig.UPLOAD_FOLDER, file.filename)
        print(file_path)
        file.save(file_path)
        return jsonify({"success": True, "file_path": file_path})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

@login_required
@admin_app.route('/', methods=['GET'])
def home():
    ''' Tela inicial do Admin '''
    user = session.get('user')
    if not user or user.get('role') != "admin":
        print("Redirecionando para o login porque o usuário não é admin ou não está logado.")
        return redirect(url_for('auth.login'))
    
    return render_template('/deshboards/dashboard-learning.html', user=user)

   

@public_endpoint
@admin_app.route('/cadastrar', methods=['POST'])
def cadastrar():
    ''' Cadastra um admin no sistema '''
    data_json = request.get_json()
    name = data_json['nome']
    cpf = data_json['CPF'] 
    password = '@dmIn-$3nh4'
    role = 'admin'
    if not UserQuerys.get_by_cpf(cpf):
        UserQuerys.create(name, cpf, password, role)
    
    return jsonify({"response": data_json}), 200

