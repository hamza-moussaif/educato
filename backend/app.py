from flask import Flask
from extensions import db, jwt, cors
import os
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from routes.auth import auth_bp
from routes.content import content_bp
from routes.test_routes import test_bp

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/dbedu'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    
    # CORS configuration
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['CORS_ORIGINS'] = ['http://localhost:3000']
    app.config['CORS_SUPPORTS_CREDENTIALS'] = True
    app.config['CORS_METHODS'] = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
    app.config['CORS_ALLOW_HEADERS'] = ['Content-Type', 'Authorization']
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    # Import and register blueprints
    from routes.auth import auth_bp
    from routes.content import content_bp
    from routes.test_routes import test_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(content_bp, url_prefix='/api/content')
    app.register_blueprint(test_bp, url_prefix='/api/test')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000, host='0.0.0.0') 