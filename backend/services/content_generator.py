import json
from services.ai_service import get_llm_response

def generate_educational_content(subject, grade):
    """Generate educational content using AI."""
    print(f"\n=== Generating content ===")
    print(f"Subject: {subject}")
    print(f"Grade: {grade}")
    
    prompt = f"""You are an expert teacher creating educational content. Create a multiple-choice question about {subject} for {grade} level students.

    Follow this format exactly:
    QUESTION: [Write a clear, engaging question]
    OPTIONS:
    1. [First option]
    2. [Second option]
    3. [Third option]
    4. [Fourth option]
    CORRECT_ANSWER: [Number 1-4]
    EXPLANATION: [Brief explanation of why this is correct]

    Guidelines:
    - Make the question clear and appropriate for {grade} level
    - Include exactly 4 options
    - Make one option clearly correct
    - Make other options plausible but incorrect
    - Keep the explanation simple and educational
    """
    
    try:
        # Get response from Ollama
        response = get_llm_response(prompt)
        print("Raw response:", response)
        
        # Validate response format
        if not response or len(response.strip()) < 10:
            raise ValueError("Invalid response from AI model")
            
        # Normalize the response for validation
        normalized_response = response.upper()
        
        # Define section headers with common typos
        section_headers = {
            'QUESTION': ['QUESTION:', 'QUESTION'],
            'OPTIONS': ['OPTIONS:', 'OPTIONS'],
            'CORRECT_ANSWER': ['CORRECT_ANSWER:', 'CORRECT_ANSWER', 'CORRECT ANSWER:', 'CORRECT ANSWER'],
            'EXPLANATION': ['EXPLANATION:', 'EXPLANATION']
        }
        
        # Check for each required section
        missing_sections = []
        for section, possible_headers in section_headers.items():
            if not any(header in normalized_response for header in possible_headers):
                missing_sections.append(section)
                
        if missing_sections:
            raise ValueError(f"Response missing required sections: {', '.join(missing_sections)}")
            
        # Check for placeholder text
        placeholder_texts = ['[WRITE', '[NUMBER', '[YOUR', '[FIRST', '[SECOND', '[THIRD', '[FOURTH']
        for placeholder in placeholder_texts:
            if placeholder in normalized_response:
                raise ValueError("Response contains placeholder text instead of actual content")
                
        return response
            
    except Exception as e:
        print(f"Failed to generate content: {str(e)}")
        raise 