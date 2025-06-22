import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqClient:
    def __init__(self):
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable is not set.")
        
        self.model = os.environ.get("GROQ_MODEL_ID")
        if not self.model:
            raise ValueError("GROQ_MODEL_ID environment variable is not set.")
        
        self.client = Groq(api_key=api_key)

    def get_chat_completion(self, messages: list, temperature: float = 0.7, max_tokens: int = 1000):
        try:
            response = self.client.chat.completions.create(messages=messages, model=self.model, temperature=temperature, max_tokens=max_tokens)
            return response.choices[0].message.content
        except Exception as e:
            return f"Error occurred: {e}"