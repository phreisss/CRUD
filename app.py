
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

# Instâncias globais das extensões
db = SQLAlchemy()

def criar_app(classe_config=Config):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(classe_config)
    
    # Inicializar extensões
    db.init_app(app)
    
    # Registrar Blueprints
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Criar tabelas do banco de dados
    with app.app_context():
        db.create_all()
    
    return app

# Importar models para que o SQLAlchemy os reconheça
from app import models
