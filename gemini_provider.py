from google import genai
from model_provider import ModelProvider


class GeminiProvider(ModelProvider):
    """Google Gemini provider."""
    
    def __init__(self, api_key: str = None, model: str = "gemini-3.5-flash"):
        self.model = model
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = genai.Client()
    
    def summarize(self, delta: str) -> str:
        interaction = self.client.interactions.create(
            model=self.model,
            input=f"You are a senior software engineer. Explain the changes made to the given git repository between the users last seen commit and the head commit, given as a git diff:\n\n{delta}"
        )
        return interaction.output_text
