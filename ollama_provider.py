import requests
from model_provider import ModelProvider


class OllamaProvider(ModelProvider):
    """Ollama local model provider."""
    
    def __init__(self, model: str, endpoint: str = "http://localhost:11434"):
        self.model = model
        self.endpoint = endpoint
    
    def summarize(self, delta: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"You are a senior software engineer. Explain the changes made to the given git repository between the users last seen commit and the head commit, given as a git diff:\n\n{delta}",
            "stream": False
        }
        response = requests.post(
            f"{self.endpoint}/api/generate",
            json=payload
        )
        response.raise_for_status()
        return response.json()["response"]
