import re
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base 

class User(UserMixin, Base):
    """Modelo de usuário para a plataforma."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String(50), nullable=False)  # 'admin', 'affiliate', 'client'

    # Relacionamento com afiliados (caso o usuário seja um afiliado)
    affiliate_details = relationship("AffiliateDetail", back_populates="user", uselist=False)

    def set_password(self, password):
        """Cria um hash seguro da senha."""
        if not self.is_valid_password(password):
            raise ValueError("A senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, números e símbolos.")
        self.password = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        """Verifica a senha."""
        return check_password_hash(self.password, password)

    def is_valid_cpf(self):
        """Valida CPF (formato e dígitos verificadores)."""
        cpf = self.cpf
        if not re.fullmatch(r"\d{11}", cpf):
            return False

        def calc_digit(cpf, weights):
            s = sum(int(cpf[i]) * weights[i] for i in range(len(weights)))
            d = (s * 10) % 11
            return 0 if d == 10 else d

        first_weights = range(10, 1, -1)
        second_weights = range(11, 2, -1)
        return (
            calc_digit(cpf, first_weights) == int(cpf[9])
            and calc_digit(cpf, second_weights) == int(cpf[10])
        )

    def is_valid_password(self, password):
        """Valida a força da senha."""
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True

    def toggle_active(self):
        """Ativar/desativar usuário."""
        self.is_active = not self.is_active

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.name,
            "cpf": self.cpf,
            "email": self.email,
            "role": self.role,
            "created_on": self.created_on,
            "last_login": self.last_login,
        }

    def __repr__(self):
        return f"<User {self.name} - {self.role}>"


class AffiliateDetail(Base):
    """Tabela para armazenar detalhes específicos dos afiliados."""
    __tablename__ = "affiliate_details"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    company_name = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    address = Column(String(255), nullable=True)

    user = relationship("User", back_populates="affiliate_details")

    def __repr__(self):
        return f"<Affiliate {self.company_name} - {self.region}>"


class Service(Base):
    """Tabela de serviços oferecidos pelos afiliados."""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True)
    affiliate_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Afiliado que cadastrou o serviço
    title = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Integer, nullable=False)  # Preço em centavos para evitar problemas de arredondamento
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Service {self.title} - R$ {self.price / 100:.2f}>"
