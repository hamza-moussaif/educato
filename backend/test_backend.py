import requests
import json
from pprint import pprint
import time

def test_backend():
    base_url = 'http://localhost:5000/api'
    
    # Utiliser un timestamp pour créer un utilisateur unique
    timestamp = int(time.time())
    test_email = f"test{timestamp}@example.com"
    
    print("\n=== Test 1: Inscription ===")
    register_data = {
        "username": f"testuser{timestamp}",
        "email": test_email,
        "password": "test123"
    }
    print("Données d'inscription:", json.dumps(register_data, indent=2))
    register_response = requests.post(f'{base_url}/auth/register', json=register_data)
    print(f"Status: {register_response.status_code}")
    print("Response:", json.dumps(register_response.json(), indent=2))
    
    print("\n=== Test 2: Connexion ===")
    login_data = {
        "email": test_email,
        "password": "test123"
    }
    print("Données de connexion:", json.dumps(login_data, indent=2))
    login_response = requests.post(f'{base_url}/auth/login', json=login_data)
    print(f"Status: {login_response.status_code}")
    print("Response:", json.dumps(login_response.json(), indent=2))
    
    if login_response.status_code == 200:
        token = login_response.json().get('token')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        print("\n=== Test 3: Génération de contenu (route test) ===")
        content_data = {
            "subject": "mathematics",
            "grade": "middle",
            "topic": "les fractions",
            "learningObjectives": "Comprendre les fractions et savoir les additionner"
        }
        print("Données de contenu:", json.dumps(content_data, indent=2))
        test_response = requests.post(
            f'{base_url}/test/generate',
            json=content_data,
            headers=headers
        )
        print(f"Status: {test_response.status_code}")
        print("Response:", json.dumps(test_response.json(), indent=2))
        
        print("\n=== Test 4: Génération de contenu (route principale) ===")
        generate_response = requests.post(
            f'{base_url}/content/generate',
            json=content_data,
            headers=headers
        )
        print(f"Status: {generate_response.status_code}")
        print("Response:", json.dumps(generate_response.json(), indent=2))
        
        print("\n=== Test 5: Vérification du token ===")
        me_response = requests.get(f'{base_url}/auth/me', headers=headers)
        print(f"Status: {me_response.status_code}")
        print("Response:", json.dumps(me_response.json(), indent=2))

if __name__ == '__main__':
    test_backend() 