from flask_login import LoginManager
from flask import Flask

from src.database.models import User

def init_app() -> Flask:
    app = Flask(__name__)

    # Configurando o LoginManager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login" 
         
    @login_manager.user_loader
    def load_user(user_id):
        session = db_connection.get_session()  # Obtenha uma sessão de banco de dados
        user = session.query(User).get(int(user_id))  # Busque o usuário pela ID
        print(user)
        session.close()  # Feche a sessão
        return user

    # Setando configurações da aplicação
    from .settings import TestingConfig
    app.config.from_object(TestingConfig)

    # Configuração do banco de dados
    from .database import Base, DBConnectionHendler
    db_connection = DBConnectionHendler()
    engine = db_connection.get_engine()
    print(engine)
    # Criando o contexto da aplicação
    with app.app_context():
        from .blueprints import auth, admin_app 
        app.register_blueprint(admin_app)
        app.register_blueprint(auth)
       
        # Criando tabelas no banco de dados
        Base.metadata.create_all(engine)

    return app
