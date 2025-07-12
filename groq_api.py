"""
groq_api.py
Wrapper for the Groq LLM API integration.
"""

import os
from typing import Dict, Any
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set.")

model_id = os.environ.get("GROQ_MODEL_ID", "llama2-70b-4096")
client = Groq(api_key=api_key)

def generate_response(prompt: str, context: Dict[str, Any]) -> str:
    """
    Generate a response using the Groq LLM API.
    Args:
        prompt (str): The prompt template
        context (dict): Context data to fill the template
    Returns:
        str: Generated response
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Ensure context is a dictionary with clean string values
        clean_context = {}
        for key, value in context.items():
            if isinstance(value, (list, dict)):
                clean_context[key] = str(value).replace('{', '').replace('}', '')
            else:
                clean_context[key] = str(value)
                
        # Ensure all required keys exist with defaults
        defaults = {
            "date": "No date available",
            "weather": "Weather unavailable",
            "calendar_events": "[]",
            "notes": "[]",
            "todos": "[]",
            "servers": "[]",
            "capabilities": "{}"
        }
        
        for key, default in defaults.items():
            if key not in clean_context:
                clean_context[key] = default
                
        # Format the prompt with context wrapped in a dict
        try:
            formatted_prompt = prompt.format(context=clean_context)
            logger.info("Successfully formatted prompt")
        except Exception as e:
            logger.error(f"Error formatting prompt: {str(e)}")
            return "I apologize, but I'm having trouble understanding the context right now. Please try again."
        
        logger.info("Creating message list...")
        messages = [
            {"role": "system", "content": "You are a helpful personal assistant using the Model Context Protocol (MCP)."},
            {"role": "user", "content": prompt.format(context=clean_context)}
        ]
        
        logger.info(f"Calling Groq API with model: {model_id}")
        
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set! Please check your .env file.")
            
        # Call Groq API
        logger.info("Making API call...")
        response = client.chat.completions.create(
            messages=messages,
            model=model_id,
            temperature=0.7,
            max_tokens=1000
        )
        
        logger.info("Successfully received response from Groq API")
        return response.choices[0].message.content
        
    except KeyError as e:
        logger.error(f"Error formatting prompt: {str(e)}")
        return f"I apologize, but I'm having trouble accessing some information right now. Could you try again or rephrase your question?"
    except Exception as e:
        import traceback
        error_msg = f"Error generating response: {str(e)}\nTraceback: {traceback.format_exc()}"
        logger.error(error_msg)
        return "I apologize, but I encountered an error. Please try again in a moment."

__all__ = ['generate_response']