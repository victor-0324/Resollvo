# pylint: disable=too-few-public-methods
"""Configurações para o projeto
Para passar determinadas variaveis e constantes para o sistemas
"""
import os
from os.path import join
from dotenv import load_dotenv


class Config:
    """Configurações globais para todo o projeto""" 
    local =  os.environ.get('local')
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')
    SECRET_KEY = os.environ.get("SECRET_KEY")
 
    DATABASE_CONNECTION = os.environ.get("DATABASE_CONNECTION")
   
class TestingConfig(Config):
    """Ambiente de testes"""
    DEBUG = False
    TESTING = True

class ProductionConfig(Config):
    """Ambiente de produção"""

    DEBUG = False
