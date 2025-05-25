import os
from app import create_app
from extensions import db

def reset_database():
    """Reset the database by removing the old one and creating a new one."""
    print("Resetting database...")
    
    # Supprimer le fichier de base de données s'il existe
    db_file = 'app.db'
    if os.path.exists(db_file):
        print(f"Removing existing database file: {db_file}")
        os.remove(db_file)
    
    # Créer l'application Flask
    app = create_app()
    
    # Créer toutes les tables
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database reset complete!")

if __name__ == '__main__':
    reset_database() 