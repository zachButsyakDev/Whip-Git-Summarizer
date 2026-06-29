import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from config import load_model_config, save_config
from gemini_provider import GeminiProvider
from openai_provider import OpenAIProvider
from ollama_provider import OllamaProvider


class TestConfig:
    """Tests for configuration management."""
    
    def test_load_model_config_no_config(self):
        """Test loading config when CUSTOM_MODEL_PROVIDER is not set."""
        with patch.dict(os.environ, {}, clear=True):
            result = load_model_config()
            assert result is None
    
    def test_load_model_config_gemini(self):
        """Test loading Gemini configuration."""
        env = {
            "CUSTOM_MODEL_PROVIDER": "gemini",
            "CUSTOM_MODEL": "gemini-3.5-flash"
        }
        with patch.dict(os.environ, env):
            result = load_model_config()
            assert result is not None
            assert result["provider"] == "gemini"
            assert result["model"] == "gemini-3.5-flash"
    
    def test_load_model_config_openai(self):
        """Test loading OpenAI configuration."""
        env = {
            "CUSTOM_MODEL_PROVIDER": "openai",
            "CUSTOM_MODEL": "gpt-4",
            "CUSTOM_API_KEY": "sk-test",
            "CUSTOM_MODEL_ENDPOINT": "https://api.openai.com/v1"
        }
        with patch.dict(os.environ, env):
            result = load_model_config()
            assert result is not None
            assert result["provider"] == "openai"
            assert result["model"] == "gpt-4"
            assert result["api_key"] == "sk-test"
            assert result["endpoint"] == "https://api.openai.com/v1"
    
    def test_load_model_config_ollama(self):
        """Test loading Ollama configuration."""
        env = {
            "CUSTOM_MODEL_PROVIDER": "ollama",
            "CUSTOM_MODEL": "llama2",
            "CUSTOM_MODEL_ENDPOINT": "http://localhost:11434"
        }
        with patch.dict(os.environ, env):
            result = load_model_config()
            assert result is not None
            assert result["provider"] == "ollama"
            assert result["model"] == "llama2"
    
    def test_save_config(self, tmp_path):
        """Test saving configuration to .env file."""
        # Save current dir and change to temp dir
        import os as os_module
        orig_cwd = os_module.getcwd()
        os_module.chdir(tmp_path)
        
        try:
            save_config("gemini", "gemini-3.5-flash", api_key="test-key")
            env_file = tmp_path / ".env"
            assert env_file.exists()
            content = env_file.read_text()
            assert "CUSTOM_MODEL_PROVIDER=gemini" in content
            assert "CUSTOM_MODEL=gemini-3.5-flash" in content
        finally:
            os_module.chdir(orig_cwd)


class TestGeminiProvider:
    """Tests for Gemini provider."""
    
    @patch("gemini_provider.genai.Client")
    def test_gemini_provider_instantiation(self, mock_client):
        """Test GeminiProvider can be instantiated."""
        provider = GeminiProvider()
        assert provider.model == "gemini-3.5-flash"
    
    @patch("gemini_provider.genai.Client")
    def test_gemini_provider_summarize(self, mock_client):
        """Test GeminiProvider summarize method."""
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        mock_interaction = MagicMock()
        mock_interaction.output_text = "Summary text"
        mock_instance.interactions.create.return_value = mock_interaction
        
        provider = GeminiProvider()
        result = provider.summarize("git diff")
        
        assert result == "Summary text"
        mock_instance.interactions.create.assert_called_once()


class TestOpenAIProvider:
    """Tests for OpenAI provider."""
    
    def test_openai_provider_instantiation(self):
        """Test OpenAIProvider can be instantiated."""
        provider = OpenAIProvider(
            api_key="sk-test",
            model="gpt-4"
        )
        assert provider.model == "gpt-4"
        assert provider.api_key == "sk-test"
        assert provider.endpoint == "https://api.openai.com/v1"
    
    @patch("openai_provider.requests.post")
    def test_openai_provider_summarize(self, mock_post):
        """Test OpenAIProvider summarize method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "OpenAI response"}}]
        }
        mock_post.return_value = mock_response
        
        provider = OpenAIProvider(api_key="sk-test", model="gpt-4")
        result = provider.summarize("git diff")
        
        assert result == "OpenAI response"
        mock_post.assert_called_once()


class TestOllamaProvider:
    """Tests for Ollama provider."""
    
    def test_ollama_provider_instantiation(self):
        """Test OllamaProvider can be instantiated."""
        provider = OllamaProvider(model="llama2")
        assert provider.model == "llama2"
        assert provider.endpoint == "http://localhost:11434"
    
    @patch("ollama_provider.requests.post")
    def test_ollama_provider_summarize(self, mock_post):
        """Test OllamaProvider summarize method."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"response": "Ollama response"}
        mock_post.return_value = mock_response
        
        provider = OllamaProvider(model="llama2")
        result = provider.summarize("git diff")
        
        assert result == "Ollama response"
        mock_post.assert_called_once()
