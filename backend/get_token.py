import requests
import json

def get_auth_token():
    # URL de l'API
    base_url = 'http://localhost:5000/api'
    
    # Données de connexion
    login_data = {
        'email': 'user@example.com',
        'password': 'test123',
        'username': 'user1'
    }
    
    # En-têtes
    headers = {
        'Content-Type': 'application/json'
    }
    
    try:
        # Essayer de s'inscrire d'abord
        print("Tentative d'inscription...")
        register_response = requests.post(f'{base_url}/auth/register', json=login_data, headers=headers)
        print(f"Réponse inscription: {register_response.text}")
        
        # Puis se connecter
        print("\nTentative de connexion...")
        login_response = requests.post(f'{base_url}/auth/login', json=login_data, headers=headers)
        print(f"Réponse connexion: {login_response.text}")
        
        if login_response.status_code == 200:
            token = login_response.json().get('token')
            print("\nToken obtenu avec succès!")
            print(f"Token: {token}")
            return token
        else:
            print(f"Erreur de connexion: {login_response.text}")
            return None
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
        return None

if __name__ == '__main__':
    token = get_auth_token()
    if token:
        # Mettre à jour le fichier test_generate.py avec le nouveau token
        with open('test_generate.py', 'r') as f:
            content = f.read()
        
        # Remplacer l'ancien token par le nouveau
        new_content = content.replace("'TON_NOUVEAU_TOKEN_ICI'", f"'{token}'")
        
        with open('test_generate.py', 'w') as f:
            f.write(new_content)
        
        print("\nFichier test_generate.py mis à jour avec le nouveau token!") 