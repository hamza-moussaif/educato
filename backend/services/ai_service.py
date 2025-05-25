import os
import requests
from typing import Dict, Any
import json
import logging
from flask import current_app

OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'mistral:latest')
OLLAMA_API_URL = f"{OLLAMA_BASE_URL}/api/generate"
MODEL_NAME = "mistral:latest"
MODEL = "mistral:latest"

def test_ollama_connection() -> Dict[str, Any]:
    """Test the connection to Ollama and return available models."""
    try:
        # Test basic connection
        print("Testing connection to Ollama...")
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        response.raise_for_status()
        
        # Get available models
        models = response.json().get('models', [])
        print(f"Available models: {models}")
        
        if not models:
            return {
                'status': 'error',
                'message': 'No models available. Please install a model first.',
                'models': []
            }
        
        # Test model generation with a simple prompt
        print("Testing model generation...")
        test_prompt = "Say 'Hello, this is a test'"
        
        # Get the model name from the first available model
        model_name = models[0].get('name', 'mistral:latest')
        print(f"Using model: {model_name}")
        
        test_request = {
            "model": model_name,
            "prompt": test_prompt,
            "stream": False
        }
        print(f"Sending test request: {test_request}")
        
        test_response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json=test_request,
            timeout=10
        )
        
        if test_response.status_code != 200:
            print(f"Error response from Ollama: {test_response.status_code}")
            print(f"Response content: {test_response.text}")
            return {
                'status': 'error',
                'message': f'Ollama returned error {test_response.status_code}: {test_response.text}',
                'models': models
            }
            
        result = test_response.json()
        print(f"Test response: {result}")
        
        return {
            'status': 'success',
            'message': 'Ollama is working correctly',
            'models': models,
            'test_response': result.get('response', '')
        }
        
    except requests.exceptions.ConnectionError:
        print("Failed to connect to Ollama. Is it running?")
        return {
            'status': 'error',
            'message': 'Failed to connect to Ollama. Is it running?',
            'models': []
        }
    except Exception as e:
        print(f"Error testing Ollama: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return {
            'status': 'error',
            'message': f'Error testing Ollama: {str(e)}',
            'models': []
        }

def get_llm_response(prompt: str, max_retries: int = 3) -> str:
    """Get a response from the LLM model via Ollama."""
    for attempt in range(max_retries):
        try:
            # First, check if Ollama is running and get available models
            try:
                models_response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=10)
                models_response.raise_for_status()
                available_models = models_response.json().get('models', [])
                
                if not available_models:
                    raise Exception("No models available. Please install a model first.")
                    
                # Use the first available model if our preferred model isn't available
                model_to_use = OLLAMA_MODEL
                if OLLAMA_MODEL not in [m.get('name', '') for m in available_models]:
                    model_to_use = available_models[0].get('name', 'mistral:latest')
                    print(f"Warning: {OLLAMA_MODEL} not found, using {model_to_use} instead")
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed to connect to Ollama. Is it running? Error: {str(e)}")
            
            # Make the actual request
            print(f"Sending request to Ollama with model: {model_to_use}")
            print(f"Prompt: {prompt}")
            
            # Simplified request format with increased timeout
            response = requests.post(
                f"{OLLAMA_BASE_URL}/api/generate",
                json={
                    "model": model_to_use,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120  # Increase timeout to 120 seconds
            )
            response.raise_for_status()
            result = response.json()
            print(f"Ollama response: {result}")
            
            if 'response' not in result:
                raise Exception("No response field in Ollama response")
                
            # Clean up the response text
            response_text = result['response'].strip()
            if not response_text:
                raise Exception("Empty response from Ollama")
                
            return response_text
            
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"Timeout occurred, retrying... (attempt {attempt + 1}/{max_retries})")
                continue
            raise Exception("Request timed out after multiple retries")
            
        except requests.exceptions.RequestException as e:
            print(f"Error getting LLM response: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response content: {e.response.text}")
            if attempt < max_retries - 1:
                print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                continue
            raise Exception(f"Failed to get response from AI model: {str(e)}")
            
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            print("Traceback:", traceback.format_exc())
            if attempt < max_retries - 1:
                print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                continue
            raise

def generate_qcm(topic: str, level: str) -> Dict[str, Any]:
    """Generate a QCM (multiple choice quiz) on a given topic."""
    print(f"Generating QCM for topic: {topic}, level: {level}")
    
    if not isinstance(topic, str):
        print(f"Topic is not a string, it's a {type(topic)}")
        raise ValueError("Topic must be a string")
        
    if not topic or not topic.strip():
        print("Topic is empty or only whitespace")
        raise ValueError("Topic cannot be empty")
        
    prompt = f"""You are an educational content generator. Generate a 5-question multiple choice quiz about "{topic.strip()}" for {level} level.
    Return ONLY a valid JSON object in this exact format, with no additional text:
    {{
        "questions": [
            {{
                "question": "Question text",
                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                "correct_answer": 0,
                "explanation": "Explanation of the correct answer"
            }}
        ]
    }}

    Important:
    - Each question MUST have exactly 4 options
    - The correct_answer must be an index (0-3) corresponding to the correct option
    - Do not include any text before or after the JSON object
    - Make sure the JSON is properly formatted with double quotes
    """
    
    try:
        print("Sending prompt to Ollama:", prompt)
        response = get_llm_response(prompt)
        print("Raw response from Ollama:", response)
        
        # Try to parse the response as JSON
        try:
            result = json.loads(response)
            print("Parsed JSON result:", result)
            
            # Validate the response format
            if 'questions' not in result:
                raise ValueError("Response missing 'questions' field")
                
            for i, question in enumerate(result['questions']):
                if 'options' not in question:
                    raise ValueError(f"Question {i+1} missing 'options' field")
                if len(question['options']) != 4:
                    raise ValueError(f"Question {i+1} must have exactly 4 options")
                if 'correct_answer' not in question:
                    raise ValueError(f"Question {i+1} missing 'correct_answer' field")
                if not isinstance(question['correct_answer'], int) or question['correct_answer'] not in range(4):
                    raise ValueError(f"Question {i+1} correct_answer must be an integer between 0 and 3")
                if 'explanation' not in question:
                    raise ValueError(f"Question {i+1} missing 'explanation' field")
            
            return result
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse response as JSON: {e}")
            print("Raw response that failed to parse:", response)
            # Try to extract JSON from the response if it's wrapped in other text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    result = json.loads(json_match.group())
                    print("Successfully extracted and parsed JSON:", result)
                    return result
                except json.JSONDecodeError:
                    pass
            raise Exception("Failed to parse QCM response as JSON")
    except Exception as e:
        print(f"Failed to generate QCM: {str(e)}")
        raise

def generate_exercise(topic: str, level: str) -> Dict[str, Any]:
    """Generate a practical exercise on a given topic."""
    print(f"Generating exercise for topic: {topic}, level: {level}")
    
    if not isinstance(topic, str):
        print(f"Topic is not a string, it's a {type(topic)}")
        raise ValueError("Topic must be a string")
        
    if not topic or not topic.strip():
        print("Topic is empty or only whitespace")
        raise ValueError("Topic cannot be empty")
        
    prompt = f"""You are an educational content generator. Generate a practical exercise about "{topic.strip()}" for {level} level.
    Return ONLY a valid JSON object in this exact format, with no additional text:
    {{
        "title": "Exercise title",
        "description": "Exercise description",
        "steps": ["Step 1", "Step 2", ...],
        "solution": "Detailed solution",
        "hints": ["Hint 1", "Hint 2", ...]
    }}"""
    
    try:
        response = get_llm_response(prompt)
        result = json.loads(response)
        print(f"Generated exercise: {result}")
        return result
    except json.JSONDecodeError as e:
        print(f"Failed to parse exercise response as JSON: {e}")
        print(f"Raw response: {response}")
        raise Exception("Failed to parse exercise response as JSON")
    except Exception as e:
        print(f"Failed to generate exercise: {str(e)}")
        raise

def generate_summary(topic: str, level: str) -> Dict[str, Any]:
    """Generate a summary sheet on a given topic."""
    print(f"Generating summary for topic: {topic}, level: {level}")
    
    if not isinstance(topic, str):
        print(f"Topic is not a string, it's a {type(topic)}")
        raise ValueError("Topic must be a string")
        
    if not topic or not topic.strip():
        print("Topic is empty or only whitespace")
        raise ValueError("Topic cannot be empty")
        
    prompt = f"""You are an educational content generator. Generate a summary sheet about "{topic.strip()}" for {level} level.
    Return ONLY a valid JSON object in this exact format, with no additional text:
    {{
        "title": "Summary title",
        "key_points": ["Point 1", "Point 2", ...],
        "main_concepts": ["Concept 1", "Concept 2", ...],
        "examples": ["Example 1", "Example 2", ...],
        "conclusion": "Conclusion text"
    }}"""
    
    try:
        response = get_llm_response(prompt)
        result = json.loads(response)
        print(f"Generated summary: {result}")
        return result
    except json.JSONDecodeError as e:
        print(f"Failed to parse summary response as JSON: {e}")
        print(f"Raw response: {response}")
        raise Exception("Failed to parse summary response as JSON")
    except Exception as e:
        print(f"Failed to generate summary: {str(e)}")
        raise

def generate_content(prompt: str) -> str:
    """Get a response from the LLM model via Ollama."""
    try:
        # First, check if Ollama is running and get available models
        try:
            models_response = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
            models_response.raise_for_status()
            available_models = models_response.json().get('models', [])
            
            if not available_models:
                raise Exception("No models available. Please install a model first.")
                
            # Use the first available model if our preferred model isn't available
            model_to_use = OLLAMA_MODEL
            if OLLAMA_MODEL not in [m.get('name', '') for m in available_models]:
                model_to_use = available_models[0].get('name', 'mistral:latest')
                print(f"Warning: {OLLAMA_MODEL} not found, using {model_to_use} instead")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to connect to Ollama. Is it running? Error: {str(e)}")
        
        # Make the actual request
        print(f"Sending request to Ollama with model: {model_to_use}")
        print(f"Prompt: {prompt}")
        
        # Simplified request format
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model_to_use,
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        result = response.json()
        print(f"Ollama response: {result}")
        
        if 'response' not in result:
            raise Exception("No response field in Ollama response")
            
        return result['response']
    except requests.exceptions.RequestException as e:
        print(f"Error getting LLM response: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        raise Exception(f"Failed to get response from AI model: {str(e)}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        print("Traceback:", traceback.format_exc())
        raise 