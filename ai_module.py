import sys
from config import load_model_config
from gemini_provider import GeminiProvider
from openai_provider import OpenAIProvider
from ollama_provider import OllamaProvider


def summarize(delta: str):
    """Summarize git diff using configured or default provider."""
    config = load_model_config()
    
    if config:
        provider_type = config["provider"]
        
        if provider_type == "gemini":
            provider = GeminiProvider(api_key=config["api_key"], model=config["model"])
        elif provider_type == "openai":
            provider = OpenAIProvider(
                api_key=config["api_key"],
                model=config["model"],
                endpoint=config.get("endpoint", "https://api.openai.com/v1")
            )
        elif provider_type == "ollama":
            provider = OllamaProvider(
                model=config["model"],
                endpoint=config.get("endpoint", "http://localhost:11434")
            )
        else:
            sys.exit(f"Unknown provider: {provider_type}")
        
        return provider.summarize(delta)
    else:
        # Fallback to Gemini if not configured
        response = input("No custom model configured. Use default Gemini? (yes/no): ").strip().lower()
        if response == "yes":
            provider = GeminiProvider()
            return provider.summarize(delta)
        else:
            sys.exit("Run 'python main.py setup' to configure a model.")

