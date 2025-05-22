import requests
import json

# URL de l'API
url = "http://localhost:5000/api/content/generate"

# Headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc0NzkzODEwMywianRpIjoiOTdkMDdiOTMtNmMxMS00NzM4LTlhZDktOTIzMTEwYTNkMTBlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NiwibmJmIjoxNzQ3OTM4MTAzLCJjc3JmIjoiMjk3YmU5MGUtYzI4MS00YjE0LTg1NjItYjc3NWM3MmRlZTIyIiwiZXhwIjoxNzQ3OTM5MDAzfQ.-opcx93bdrZfjE68hghvUXXwr_NaWTzJvuHbhiVZCuk"
}

# Données à envoyer
data = {
    "subject": "mathematics",
    "grade": "middle",
    "topic": "les fractions",
    "learningObjectives": "Comprendre les fractions et savoir les additionner"
}

print("Envoi de la requête...")
print(f"URL: {url}")
print(f"Headers: {json.dumps(headers, indent=2)}")
print(f"Data: {json.dumps(data, indent=2)}")

try:
    # Envoi de la requête
    response = requests.post(url, json=data, headers=headers)
    
    # Affichage de la réponse
    print("\nRéponse reçue:")
    print(f"Status code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Content: {response.text}")
    
    # Si la réponse est une erreur, afficher plus de détails
    if response.status_code >= 400:
        print("\nDétails de l'erreur:")
        print(f"URL finale: {response.url}")
        print(f"Method: {response.request.method}")
        print(f"Request Headers: {dict(response.request.headers)}")
        print(f"Request Body: {response.request.body}")
        
except requests.exceptions.RequestException as e:
    print(f"\nErreur lors de l'envoi de la requête: {str(e)}") 