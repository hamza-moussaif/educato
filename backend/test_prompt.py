import requests
import json

def test_prompt_generation():
    """Test the prompt generation with Ollama."""
    print("\n=== Testing Prompt Generation ===")
    
    # Simpler test prompt
    prompt = """Generate a simple math question with 4 options. Return ONLY a JSON object in this format:
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "correct_answer": 1
    }"""

    try:
        # Make request to Ollama
        print("Sending request to Ollama...")
        print("Using model: mistral")
        print("Prompt:", prompt)
        
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 200
                }
            },
            timeout=60  # Increased timeout
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("\nRaw response:", result)
            
            if 'response' in result:
                response_text = result['response'].strip()
                print("\nCleaned response text:", response_text)
                
                try:
                    # Try to parse as JSON
                    json_response = json.loads(response_text)
                    print("\nSuccessfully parsed JSON response:", json.dumps(json_response, indent=2))
                    return True
                except json.JSONDecodeError as e:
                    print("\nFailed to parse response as JSON")
                    print("JSON Error:", str(e))
                    print("Response text:", response_text)
                    return False
            else:
                print("\nNo 'response' field in the result")
                print("Full result:", result)
                return False
        else:
            print(f"\nError: API returned status code {response.status_code}")
            print("Error response:", response.text)
            return False
            
    except requests.exceptions.Timeout:
        print("\nError: Request timed out after 60 seconds")
        print("This might indicate that:")
        print("1. The model is still loading")
        print("2. The request is too complex")
        print("3. Ollama is not responding properly")
        return False
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to Ollama")
        print("Please check if Ollama is running by executing 'ollama list'")
        return False
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return False

if __name__ == "__main__":
    print("Starting prompt generation test...")
    success = test_prompt_generation()
    print("\nTest completed:", "Success" if success else "Failed") 