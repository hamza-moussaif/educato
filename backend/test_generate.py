import requests
import json

def test_generate_content():
    # En-têtes
    headers = {
        'Content-Type': 'application/json'
    }
    
    # Données de test
    data = {
        "subject": "mathematics",
        "grade": "middle",
        "topic": "les fractions",
        "learningObjectives": "Comprendre les fractions et savoir les additionner"
    }
    
    print("Sending request with data:", json.dumps(data, indent=2))
    
    # Envoyer la requête à la nouvelle route /api/test/generate
    response = requests.post(
        'http://localhost:5000/api/test/generate',
        json=data,
        headers=headers
    )
    
    print(f"Status code: {response.status_code}")
    print("Response:", json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    test_generate_content() 