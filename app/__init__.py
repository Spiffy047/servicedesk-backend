from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///servicedesk.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Register blueprints
    from app.routes.tickets import tickets_bp
    from app.routes.files import files_bp
    
    app.register_blueprint(tickets_bp, url_prefix='/api/tickets')
    app.register_blueprint(files_bp, url_prefix='/api/files')
    
    return app