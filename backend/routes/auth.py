from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User
from extensions import db

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def handle_options_request():
    """Handle OPTIONS request for CORS preflight."""
    response = jsonify({'status': 'ok'})
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

@auth_bp.route('/register', methods=['POST', 'OPTIONS'])
def register():
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'token': access_token,
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        if 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
            
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            access_token = create_access_token(identity=user.id)
            return jsonify({
                'token': access_token,
                'user': user.to_dict()
            }), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET', 'OPTIONS'])
@jwt_required()
def get_current_user():
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    try:
        print("\n=== Headers reçus (auth/me) ===")
        print(dict(request.headers))
        
        user_id = get_jwt_identity()
        print(f"User ID from token: {user_id}")
        
        if not user_id:
            print("No user ID found in token")
            return jsonify({'error': 'No user ID found in token'}), 401
            
        user = User.query.get(user_id)
        if not user:
            print(f"User not found for ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        
        print(f"User found: {user.to_dict()}")
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        print(f"Error in get_current_user: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({'error': 'Failed to get user information'}), 500 