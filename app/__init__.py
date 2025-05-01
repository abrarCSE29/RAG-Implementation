from flask import Flask
from app.api.routes import api_bp

def create_app(config_object=None):
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app