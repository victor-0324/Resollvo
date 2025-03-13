# pylint: disable=no-value-for-parameter
"""Routes for user authentication."""

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
)
from flask_login import  login_user, logout_user
from src.database.models import User
from src.database.querys import UserQuerys


auth = Blueprint(
    "auth",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@current_app.before_request
def check_valid_login():
    """Check if user have a valid login."""
    login_valid = "_user_id" in session  # or whatever you use to check valid login
    rules = (
        request.endpoint
        and "static" not in request.endpoint
        and not login_valid
        and not getattr(
            current_app.view_functions[request.endpoint], "is_public", False
        )
    )

    match rules:
        case True:
            return render_template("login.html")


def public_endpoint(function):
    """Decoretor for public routes"""
    function.is_public = True
    return function


@public_endpoint
@auth.route("/login", methods=["GET", "POST"])
@public_endpoint
def login():
    """Login user in system"""
    if request.method == "POST":
        data = request.get_json()
        print(f"Dados recebidos na requisição: {data}")  # Log dos dados recebidos

        cpf = data.get("cpf")
        password = data.get("password")

        # Buscar o usuário no banco
        user = UserQuerys.get_by_cpf(cpf)
        print(f"Usuário encontrado no banco: {user}")  # Log do usuário retornado pelo banco

        if user and user.check_password(password):  # Verifica credenciais
            print(f"Usuário {user.name} autenticado com sucesso.")
            login_user(user)  # Loga o usuário
            session['user'] = user.to_dict()  # Armazena o usuário na sessão
          
            if user.role == "admin":
                print("Redirecionando para o painel de admin.")
                return jsonify({"redirect": url_for('admin_app.administrador')}), 200

            elif user.role == "motorista":
                print("Redirecionando para faturamentos.")
                return jsonify({"redirect": url_for('motoristas_app.faturamentos')}), 200

            else:
                print("Papel do usuário desconhecido.")
                return jsonify({"message": "Papel do usuário desconhecido."}), 403

        # Se CPF ou senha estiverem incorretos
        print("Falha na autenticação: CPF ou senha incorretos.")
        return jsonify({"message": "CPF ou senha incorretos."}), 401

    # Renderiza a página de login em requisições GET
    return render_template("login.html")



@auth.route("/create_user", methods=["POST"])
def create_user():
    """Register new user."""
    print(request.form, )

    name = request.form.get("name")
    cpf = request.form.get("cpf")
    password = request.form.get("password")
    if not UserQuerys.get_by_cpf(cpf):
        UserQuerys.create(name, cpf, password)

    return jsonify({"response": name }), 200 


@auth.route("/logout", methods=["GET", "POST"])
def logout():
    """Logout user."""
    logout_user()
    return render_template("login.html")


@auth.route("/user_register", methods=["GET"])
@public_endpoint
def user_register():
    """Register new user."""
    return render_template("pages/auth/register.html")


@auth.route("/home", methods=["GET"])
@public_endpoint
def home():
    """Register new user."""
    return render_template("dashboards/index.html")