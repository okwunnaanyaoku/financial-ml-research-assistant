import os
import time
from typing import Optional
import google.genai as genai
try:
    from google.genai import types as genai_types
except ImportError:
    genai_types = None
from config import config

class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv(config.llm_api_key_env)
        self.client = None
        self.model = config.llm_model
        self.timeout = config.llm_timeout
        self.max_retries = 3
        self.temperature = config.llm_temperature

        # Initialize client only if API key is available
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini client: {e}")

    def generate_response(self, prompt: str, temperature: Optional[float] = None) -> str:
        """Generate response using Gemini model with retry logic"""
        if not self.client:
            return "Error: Gemini client not initialized (missing API key)"

        use_temperature = temperature if temperature is not None else self.temperature

        for attempt in range(self.max_retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt,
                    config=genai_types.GenerateContentConfig(
                        temperature=use_temperature,
                        max_output_tokens=2048
                    )
                )
                return response.text

            except Exception as e:
                if attempt == self.max_retries - 1:
                    return f"Gemini API failed after {self.max_retries} attempts: {e}"
                time.sleep(2 ** attempt)  # Exponential backoff

        return "Error generating response"

    def is_available(self) -> bool:
        """Check if Gemini client is properly configured"""
        return self.client is not None and self.api_key is not None

# Global instance
gemini_client = GeminiClient()