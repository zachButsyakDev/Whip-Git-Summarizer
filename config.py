import os
from dotenv import load_dotenv
from pathlib import Path


def get_config_path():
    """Get config file path with priority: ~/.whip/.env → ~/.config/whip/.env → ./.env"""
    home = Path.home()
    
    # Primary: ~/.whip/.env
    whip_dir = home / ".whip"
    whip_env = whip_dir / ".env"
    if whip_env.exists():
        return whip_env
    
    # Secondary: ~/.config/whip/.env
    config_dir = home / ".config" / "whip"
    config_env = config_dir / ".env"
    if config_env.exists():
        return config_env
    
    # Fallback: current directory
    cwd_env = Path(".env")
    if cwd_env.exists():
        return cwd_env
    
    # Default to ~/.whip/.env for new configs
    return whip_env


def load_model_config():
    """Load and validate model configuration from environment variables."""
    env_path = get_config_path()
    load_dotenv(env_path)
    
    provider = os.getenv("CUSTOM_MODEL_PROVIDER")
    if not provider:
        return None
    
    config = {
        "provider": provider.lower(),
        "model": os.getenv("CUSTOM_MODEL"),
        "api_key": os.getenv("CUSTOM_API_KEY"),
        "endpoint": os.getenv("CUSTOM_MODEL_ENDPOINT")
    }
    
    # Validate required fields per provider
    if config["provider"] == "gemini":
        if not config["model"]:
            config["model"] = "gemini-3.5-flash"
    elif config["provider"] == "openai":
        if not config["model"] or not config["api_key"]:
            return None
    elif config["provider"] == "ollama":
        if not config["model"]:
            return None
        if not config["endpoint"]:
            config["endpoint"] = "http://localhost:11434"
    else:
        return None
    
    return config


def save_config(provider: str, model: str, api_key: str = None, endpoint: str = None):
    """Save configuration to .env file."""
    env_path = get_config_path()
    
    # Create parent directories if needed
    env_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Read existing content
    existing = {}
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, _, value = line.partition("=")
                    existing[key] = value
    
    # Update with new values
    existing["CUSTOM_MODEL_PROVIDER"] = provider
    existing["CUSTOM_MODEL"] = model
    if api_key:
        existing["CUSTOM_API_KEY"] = api_key
    if endpoint:
        existing["CUSTOM_MODEL_ENDPOINT"] = endpoint
    
    # Write back to .env
    with open(env_path, 'w') as f:
        for key, value in existing.items():
            f.write(f"{key}={value}\n")
