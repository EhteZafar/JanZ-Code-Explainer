"""
Groq API Integration Module
Handles communication with LLaMA 3.3 70B Versatile model via Groq API
"""

import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Model configuration
MODEL_NAME = "llama-3.3-70b-versatile"
MAX_TOKENS = 2048
TEMPERATURE = 0.7
TIMEOUT = 30  # seconds


def create_explanation_prompt(code: str) -> str:
    """
    Creates a structured prompt for the LLM to explain code.
    
    Args:
        code: The code snippet to explain
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are an expert programming instructor. Analyze the following code and provide a clear, comprehensive explanation.

Your explanation should include:
1. **Overview**: What does this code do? (1-2 sentences)
2. **Detailed Breakdown**: Explain the code step-by-step, covering:
   - Key variables and their purposes
   - Important functions/methods and their roles
   - Logic flow and control structures
   - Any algorithms or patterns used
3. **Key Concepts**: Highlight important programming concepts demonstrated
4. **Potential Issues**: Note any potential bugs, edge cases, or improvements (if applicable)

Code to explain:
```
{code}
```

Provide a well-structured, educational explanation that helps the reader understand both what the code does and why it's written this way."""
    
    return prompt


async def get_code_explanation(code: str) -> dict:
    """
    Sends code to LLaMA 3.3 70B via Groq API and returns explanation.
    
    Args:
        code: The code snippet to explain
        
    Returns:
        Dictionary with explanation or error message
        {
            "success": bool,
            "explanation": str,
            "error": str (optional)
        }
    """
    try:
        # Validate input
        if not code or not code.strip():
            return {
                "success": False,
                "error": "No code provided. Please paste code to explain."
            }
        
        if len(code) > 10000:
            return {
                "success": False,
                "error": "Code is too long. Please provide a snippet under 10,000 characters."
            }
        
        # Check API key
        if not os.getenv("GROQ_API_KEY"):
            return {
                "success": False,
                "error": "GROQ_API_KEY not configured. Please check your .env file."
            }
        
        # Create prompt
        prompt = create_explanation_prompt(code)
        
        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert programming instructor who provides clear, accurate, and educational code explanations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model=MODEL_NAME,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            timeout=TIMEOUT,
            top_p=1,
            stream=False
        )
        
        # Extract explanation
        explanation = chat_completion.choices[0].message.content
        
        return {
            "success": True,
            "explanation": explanation.strip()
        }
        
    except Exception as e:
        error_message = str(e)
        
        # Handle specific error cases
        if "api_key" in error_message.lower():
            error_message = "Invalid API key. Please check your GROQ_API_KEY in .env file."
        elif "timeout" in error_message.lower():
            error_message = "Request timed out. Please try again with a smaller code snippet."
        elif "rate_limit" in error_message.lower():
            error_message = "Rate limit exceeded. Please wait a moment and try again."
        else:
            error_message = f"Error communicating with AI service: {error_message}"
        
        return {
            "success": False,
            "error": error_message
        }


def test_groq_connection() -> bool:
    """
    Tests the connection to Groq API.
    
    Returns:
        True if connection successful, False otherwise
    """
    try:
        test_code = "print('Hello, World!')"
        prompt = create_explanation_prompt(test_code)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model=MODEL_NAME,
            max_tokens=100,
            timeout=10
        )
        
        return chat_completion.choices[0].message.content is not None
        
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False
