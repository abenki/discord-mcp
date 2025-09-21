import json
import os
import requests
from typing import Optional, Dict, Any


class LLMClient:
    """Client for interacting with the Ollama API."""

    def __init__(self) -> None:
        """Initialize the LLMClient with configuration from environment variables.

        Environment Variables:
            OLLAMA_API_URL: The URL of the Ollama API. Defaults to 'http://localhost:11434/api/generate'.
            OLLAMA_MODEL: The name of the model to use. Defaults to 'qwen2.5:14b'.
        """
        # Load configuration from environment variables with sensible defaults
        self.api_url: str = os.getenv(
            "OLLAMA_API_URL", "http://localhost:11434/api/generate")
        self.model_name: str = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")

        print("LLM Client initialized:")
        print(f"  API URL: {self.api_url}")
        print(f"  Model: {self.model_name}")

    async def get_response(self, prompt: str) -> Optional[Dict[str, Any]]:
        """Get a response from the LLM for the given prompt.

        Args:
            prompt (str): The prompt to send to the LLM.

        Returns:
            dict: The JSON response from the LLM.
            None: If there is an error calling the API or decoding the JSON response.
        """
        try:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,  # We want the full response at once
                    "format": "json"  # We expect a JSON response
                },
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()  # Raise an exception for bad status codes
            # The actual JSON response is a string inside the 'response' key
            return json.loads(response.json()["response"])
        except requests.exceptions.RequestException as e:
            print(f"Error calling Ollama API: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from Ollama: {e}")
            return None
