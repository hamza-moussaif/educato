import json
from services.ai_service import get_llm_response

def generate_educational_content(subject, grade, topic=None, learning_objectives=None):
    """Generate educational content using AI."""
    print(f"\n=== Generating content ===")
    print(f"Subject: {subject}")
    print(f"Grade: {grade}")
    print(f"Topic: {topic}")
    print(f"Learning objectives: {learning_objectives}")
    
    # Construire le prompt
    prompt = f"""You are an educational content generator. Generate a 5-question multiple choice quiz about "{subject}" for {grade} level.
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
    - Generate 5 questions total
    """
    
    try:
        # Appeler l'API Ollama
        response = get_llm_response(prompt)
        print("Raw response:", response)
        
        # Parser la réponse JSON
        try:
            content = json.loads(response)
            print("Parsed content:", content)
            
            # Valider le format
            if 'questions' not in content:
                raise ValueError("Response missing 'questions' field")
                
            for i, question in enumerate(content['questions']):
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
            
            return content
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse response as JSON: {e}")
            print("Raw response that failed to parse:", response)
            # Essayer d'extraire le JSON de la réponse
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    content = json.loads(json_match.group())
                    print("Successfully extracted and parsed JSON:", content)
                    return content
                except json.JSONDecodeError:
                    pass
            raise ValueError("Failed to parse AI response as JSON")
            
    except Exception as e:
        print(f"Error generating content: {str(e)}")
        raise 