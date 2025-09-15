import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-desenvolvimento'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "..", "tarefas.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TAREFAS_POR_PAGINA = 10
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    @staticmethod
    def init_app(app):
        pass

class ConfigDesenvolvimento(Config):
    DEBUG = True

class ConfigTestes(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ConfigProducao(Config):
    DEBUG = False

configuracoes = {
    'desenvolvimento': ConfigDesenvolvimento,
    'testes': ConfigTestes,
    'producao': ConfigProducao,
    'padrao': ConfigDesenvolvimento
}