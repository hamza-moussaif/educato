import requests
import json

def test_ollama_connection():
    """Test the connection to Ollama API."""
    url = "http://localhost:11434/api/tags"
    print("\nTesting Ollama connection...")
    try:
        response = requests.get(url, timeout=5)
        print("Status code:", response.status_code)
        print("Response:", response.text)
        return response.status_code == 200
    except Exception as e:
        print("Error:", str(e))
        return False

def test_generate_content():
    # D'abord, tester la connexion à Ollama
    if not test_ollama_connection():
        print("\nOllama is not running or not accessible. Please start Ollama first.")
        return

    # Ensuite, tester la génération de contenu
    url = "http://localhost:5000/api/content/generate"
    
    # Login pour obtenir le token
    login_url = "http://localhost:5000/api/auth/login"
    login_data = {
        "email": "test@example.com",
        "password": "testpassword"
    }
    
    try:
        login_response = requests.post(login_url, json=login_data)
        if login_response.status_code != 200:
            print("Login failed:", login_response.text)
            return
            
        token = login_response.json().get('token')
        if not token:
            print("No token received from login")
            return
            
        # Headers avec le token d'authentification
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        data = {
            "subject": "mathematics",
            "grade": "middle"
        }
        
        print("\nTesting content generation...")
        print("URL:", url)
        print("Headers:", headers)
        print("Data:", data)
        
        response = requests.post(url, headers=headers, json=data)
        print("\nResponse status:", response.status_code)
        print("Response headers:", dict(response.headers))
        print("Response body:", response.text)
        
        if response.status_code == 200:
            print("\nSuccess! Content generated successfully.")
        else:
            print("\nError! Failed to generate content.")
            
    except Exception as e:
        print("\nError occurred:", str(e))

if __name__ == "__main__":
    test_generate_content() 