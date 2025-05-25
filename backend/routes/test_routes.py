from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.content_generator import generate_educational_content
import json
from models.models import User
from extensions import db

test_bp = Blueprint('test', __name__, url_prefix='/api/test')

@test_bp.route('/generate', methods=['POST'])
# @jwt_required()  # Désactivé temporairement
def test_generate():
    try:
        print("\n=== Headers reçus ===")
        print(dict(request.headers))
        
        # Récupérer les données brutes
        data = request.get_json(force=True, silent=True)
        print("\n=== Données reçues (test_generate) ===")
        print(data)
        print(f"Type des données: {type(data)}")
        
        # Vérifier que les données sont présentes
        if not data:
            return jsonify({'error': 'Aucune donnée reçue'}), 400
            
        # Extraire les champs avec des valeurs par défaut
        subject = str(data.get('subject', ''))
        grade = str(data.get('grade', ''))
        topic = str(data.get('topic', ''))
        learning_objectives = str(data.get('learningObjectives', ''))
        
        print("\n=== Champs extraits (test_generate) ===")
        print(f"subject: {subject} (type: {type(subject)})")
        print(f"grade: {grade} (type: {type(grade)})")
        print(f"topic: {topic} (type: {type(topic)})")
        print(f"learning_objectives: {learning_objectives} (type: {type(learning_objectives)})")
        
        # Vérifier que les champs ne sont pas vides
        if not all([subject, grade, topic, learning_objectives]):
            missing_fields = []
            if not subject: missing_fields.append('subject')
            if not grade: missing_fields.append('grade')
            if not topic: missing_fields.append('topic')
            if not learning_objectives: missing_fields.append('learningObjectives')
            return jsonify({
                'error': 'Tous les champs sont requis',
                'missing_fields': missing_fields
            }), 400
            
        # Générer le contenu
        try:
            print(f'AVANT GENERATE (test_generate): subject={subject!r} type={type(subject)}')
            content = generate_educational_content(
                subject=subject,
                grade=grade,
                topic=topic,
                learning_objectives=learning_objectives
            )
            print("Contenu généré avec succès:", json.dumps(content, indent=2))
            return jsonify(content), 200
        except Exception as e:
            print(f"Erreur lors de la génération (test_generate): {str(e)}")
            return jsonify({
                'error': str(e),
                'details': {
                    'subject': subject,
                    'grade': grade,
                    'topic': topic,
                    'learning_objectives': learning_objectives
                }
            }), 500
            
    except Exception as e:
        print(f"Erreur dans la route (test_generate): {str(e)}")
        return jsonify({
            'error': str(e),
            'type': type(e).__name__
        }), 500

@test_bp.route('/users', methods=['GET'])
def list_users():
    """List all users (development only)"""
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@test_bp.route('/create-test-user', methods=['POST'])
def create_test_user():
    """Create a test user (development only)"""
    try:
        # Vérifier si l'utilisateur existe déjà
        test_user = User.query.filter_by(email='test@example.com').first()
        if test_user:
            return jsonify({
                'message': 'Test user already exists',
                'user': test_user.to_dict()
            }), 200

        # Créer un nouvel utilisateur de test
        from werkzeug.security import generate_password_hash
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('password123')
        )
        db.session.add(test_user)
        db.session.commit()

        return jsonify({
            'message': 'Test user created successfully',
            'user': test_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 