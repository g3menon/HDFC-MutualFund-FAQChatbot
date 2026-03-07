import logging
from google import genai
from google.genai import types
from phase4.rag.config import GEMINI_API_KEY, GEMINI_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS

logger = logging.getLogger("phase4")

class LLMClient:
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_response(self, prompt: str) -> str:
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=LLM_TEMPERATURE,
                    max_output_tokens=LLM_MAX_TOKENS,
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"Error generating LLM response: {e}")
            return "I'm sorry, an error occurred while generating the response."
