import requests
import json

BASE_URL = 'http://localhost:5000'

def test_register():
    print("\nTesting registration...")
    data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = requests.post(f'{BASE_URL}/api/auth/register', json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json() if response.status_code == 201 else None

def test_login():
    print("\nTesting login...")
    data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    response = requests.post(f'{BASE_URL}/api/auth/login', json=data)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json() if response.status_code == 200 else None

def test_generate_content(token):
    print("\nTesting content generation...")
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'subject': 'mathematics',
        'grade': 'middle',
        'topic': 'les fractions',
        'learningObjectives': 'Comprendre les fractions et savoir les additionner'
    }
    response = requests.post(f'{BASE_URL}/api/content/generate', json=data, headers=headers)
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")
    return response.json() if response.status_code == 200 else None

if __name__ == '__main__':
    # Test registration
    register_response = test_register()
    
    # Test login
    login_response = test_login()
    if login_response and 'token' in login_response:
        token = login_response['token']
        
        # Test content generation
        content_response = test_generate_content(token) 