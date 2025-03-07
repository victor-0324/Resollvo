"""User Querys"""

from typing import List

from src.database.db_connection import db_connector
from src.database.models import User
from datetime import datetime

class UserQuerys:
    """querys from users"""

    @classmethod
    @db_connector
    def get_by_id(cls, connection, user_id):
        """Get a User by id."""
        return connection.session.query(User).filter_by(id=int(user_id))

    @classmethod
    @db_connector
    def get_by_cpf(cls, connection, cpf) -> List:
        """Select a user by CPF"""
        return connection.session.query(User).filter_by(cpf=cpf).first()

    @classmethod
    @db_connector
    def create(cls, connection, name, cpf, password, role) -> User:
        """Create_user"""
        user = User(
            name=name,
            cpf=cpf,
            created_on=datetime.now(),
            role=role
        )
        user.set_password(password)
        connection.session.add(user)
        connection.session.commit()  
        return user
        # Função de callback do user_loader
    