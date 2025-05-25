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
        print("\n=== Register request received ===")
        print("Headers:", dict(request.headers))
        print("Content-Type:", request.content_type)
        
        data = request.get_json()
        print("Request data:", data)
        
        if not data:
            print("No data provided")
            return jsonify({'error': 'No data provided'}), 400
            
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data:
                print(f"Missing field: {field}")
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Check if email already exists
        existing_email = User.query.filter_by(email=data['email']).first()
        if existing_email:
            print(f"Email already registered: {data['email']}")
            return jsonify({'error': 'Email already registered'}), 400
            
        # Check if username already exists
        existing_username = User.query.filter_by(username=data['username']).first()
        if existing_username:
            print(f"Username already taken: {data['username']}")
            return jsonify({'error': 'Username already taken'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=data['password']
        )
        
        print("Creating new user:", user.to_dict())
        db.session.add(user)
        db.session.commit()
        
        # Create access token
        access_token = create_access_token(identity=user.id)
        
        response_data = {
            'message': 'User registered successfully',
            'token': access_token,
            'user': user.to_dict()
        }
        print("Registration successful:", response_data)
        
        return jsonify(response_data), 201
        
    except Exception as e:
        db.session.rollback()
        print("Registration error:", str(e))
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    try:
        print("\n=== Login request received ===")
        print("Headers:", dict(request.headers))
        print("Content-Type:", request.content_type)
        
        data = request.get_json()
        print("Request data:", data)
        
        if not data:
            print("No data provided")
            return jsonify({'error': 'No data provided'}), 400
            
        if 'email' not in data or 'password' not in data:
            print("Missing email or password")
            return jsonify({'error': 'Email and password are required'}), 400
            
        user = User.query.filter_by(email=data['email']).first()
        print(f"User found: {user is not None}")
        
        if user:
            print(f"User details: {user.to_dict()}")
            print(f"Attempting to verify password: {data['password']}")
            
            if not user or not user.check_password(data['password']):
                print('Password verification failed (plain text)')
                return jsonify({'message': 'Invalid credentials'}), 401
            
            access_token = create_access_token(identity=user.id)
            response_data = {
                'token': access_token,
                'user': user.to_dict()
            }
            print("Login successful:", response_data)
            return jsonify(response_data), 200
        
        print("Invalid credentials")
        return jsonify({'error': 'Invalid credentials'}), 401
        
    except Exception as e:
        print("Login error:", str(e))
        import traceback
        print("Traceback:", traceback.format_exc())
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

@auth_bp.route('/reset-password', methods=['POST', 'OPTIONS'])
def reset_password():
    if request.method == 'OPTIONS':
        return handle_options_request()
        
    try:
        print("\n=== Password reset request received ===")
        data = request.get_json()
        
        if not data or 'email' not in data or 'new_password' not in data:
            return jsonify({'error': 'Email and new password are required'}), 400
            
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        print(f"Resetting password for user: {user.username}")
        
        # Update the password
        user.password = data['new_password']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Password reset successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print("Password reset error:", str(e))
        return jsonify({'error': str(e)}), 500 