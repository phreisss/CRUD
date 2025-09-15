from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app(classe_config=Config):
    app = Flask(__name__)
    app.config.from_object(classe_config)
    db.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    with app.app_context():
        db.create_all()
    
    return app