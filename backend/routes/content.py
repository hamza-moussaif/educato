from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import Request, Content
from extensions import db
from services.content_generator import generate_educational_content
import json
import os

content_bp = Blueprint('content', __name__, url_prefix='/api/content')

# Variable globale pour le mode développement
IS_DEVELOPMENT = True  # À mettre à False en production

@content_bp.route('/generate', methods=['GET', 'POST', 'OPTIONS'])
def generate_content():
    """Generate a QCM exercise."""
    print("\n=== /api/content/generate called ===")
    print("Request method:", request.method)
    print("Request headers:", dict(request.headers))
    
    # Gérer les requêtes OPTIONS pour CORS
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response
        
    # Gérer les requêtes GET
    if request.method == 'GET':
        return jsonify({'message': 'This endpoint accepts POST requests'}), 200
        
    try:
        # En mode développement, utiliser un ID utilisateur de test
        user_id = 1 if IS_DEVELOPMENT else get_jwt_identity()
        
        # Récupérer les données
        if not request.is_json:
            print("Request is not JSON")
            return jsonify({'error': 'Content-Type must be application/json'}), 400
            
        data = request.get_json()
        print("Received data:", data)
        print("Data type:", type(data))
        
        if not data:
            print("No data provided")
            return jsonify({'error': 'No data provided'}), 400
            
        # Extraire les champs
        subject = data.get('subject')
        grade = data.get('grade')
        
        print(f"Subject: {subject}, Type: {type(subject)}")
        print(f"Grade: {grade}, Type: {type(grade)}")
        
        # Vérifier que les champs existent et ne sont pas vides
        if not subject or not isinstance(subject, str):
            print(f"Invalid subject: {subject}")
            return jsonify({'error': 'Subject must be a non-empty string'}), 422
        if not grade or not isinstance(grade, str):
            print(f"Invalid grade: {grade}")
            return jsonify({'error': 'Grade must be a non-empty string'}), 422
            
        # Nettoyer les chaînes
        subject = subject.strip()
        grade = grade.strip()
        
        if not subject or not grade:
            print("Empty strings after stripping")
            return jsonify({'error': 'Subject and grade cannot be empty'}), 422
            
        # Générer le contenu
        try:
            print("Generating content with:", {"subject": subject, "grade": grade})
            content = generate_educational_content(
                subject=subject,
                grade=grade
            )
            print("Generated content:", content)
            
            # Créer une nouvelle requête
            request_obj = Request(
                user_id=user_id,
                topic=subject,
                level=grade,
                content_type='qcm'
            )
            db.session.add(request_obj)
            db.session.flush()
            
            # Créer le contenu
            content_obj = Content(
                user_id=user_id,
                request_id=request_obj.id,
                title=f"QCM {subject} - {grade}",
                content_type='qcm',
                content_data=content
            )
            db.session.add(content_obj)
            db.session.commit()
            
            response = jsonify({
                'message': 'QCM generated successfully',
                'content': content,
                'request_id': request_obj.id,
                'content_id': content_obj.id
            })
            
            # Ajouter les headers CORS à la réponse
            response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            
            return response, 200
            
        except Exception as e:
            db.session.rollback()
            print(f"Error generating content: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
    except Exception as e:
        print(f"Error in generate_content: {str(e)}")
        return jsonify({'error': str(e)}), 500

@content_bp.route('/test-ai', methods=['GET'])
def test_ai():
    """Test endpoint to check AI service connection."""
    try:
        from services.ai_service import test_ollama_connection
        result = test_ollama_connection()
        return jsonify(result), 200 if result['status'] == 'success' else 500
    except Exception as e:
        print(f"Error testing AI service: {str(e)}")
        return jsonify({'error': str(e)}), 500 