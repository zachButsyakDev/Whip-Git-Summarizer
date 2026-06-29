import requests
from model_provider import ModelProvider


class OpenAIProvider(ModelProvider):
    """OpenAI and OpenAI-compatible provider."""
    
    def __init__(self, api_key: str, model: str, endpoint: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint
    
    def summarize(self, delta: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a senior software engineer."
                },
                {
                    "role": "user",
                    "content": f"Explain the changes made to the given git repository between the users last seen commit and the head commit, given as a git diff:\n\n{delta}"
                }
            ]
        }
        response = requests.post(
            f"{self.endpoint}/chat/completions",
            json=payload,
            headers=headers
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
