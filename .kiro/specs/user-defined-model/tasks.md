  Task Breakdown

  Task 1: Create model provider abstraction layer

  - Objective: Build an abstract interface for different AI providers
  - Implementation: Create a ModelProvider class/strategy pattern that handles Gemini,
  OpenAI-compatible, and Ollama backends
  - Each provider implements a summarize(delta: str) -> str method
  - Parse model configuration from environment variables to determine which provider to instantiate
  - Test: Unit test that each provider can be instantiated with correct config

  Task 2: Implement configuration management

  - Objective: Load and validate model configuration from .env
  - Implementation: Create a config.py module with a load_model_config() function that reads
  CUSTOM_MODEL, CUSTOM_API_KEY, CUSTOM_MODEL_PROVIDER, CUSTOM_MODEL_ENDPOINT from environment
  - Return a dict with model settings or None if not configured
  - Include validation logic (e.g., check required fields per provider type)
  - Test: Unit test that config loads correctly from .env

  Task 3: Add setup command to main.py

  - Objective: Allow interactive model configuration
  - Implementation: Add a new CLI command python main.py setup that prompts user for:
    - Provider type (gemini/openai/ollama)
    - Model name
    - API key (optional for local Ollama)
    - Endpoint URL (optional for cloud providers, required for local)

  - Write responses to .env file (preserve existing entries)
  - Test: Verify .env is updated correctly with new values

  Task 4: Refactor ai_module.py to use configuration

  - Objective: Replace hardcoded Gemini call with configurable provider routing
  - Implementation: Update summarize(delta: str) to:
    1. Call config.load_model_config() to get user's model
    2. If configured, instantiate and use appropriate provider
    3. If not configured, ask user if they want to use Gemini (yes/no)
    4. If yes, use default Gemini; if no, exit with message to run setup

  - Test: Integration test that summarize works with multiple provider types

  Task 5: Implement Gemini provider class

  - Objective: Wrap existing Gemini logic in provider abstraction
  - Implementation: Create GeminiProvider class that mirrors current summarize() logic
  - Implement summarize(delta: str) -> str method using genai.Client()
  - Test: Verify it produces same output as current implementation

  Task 6: Implement OpenAI-compatible provider class

  - Objective: Support OpenAI and OpenAI-compatible APIs
  - Implementation: Create OpenAIProvider class that uses requests or openai library
  - Take endpoint URL, API key, and model name from config
  - Implement summarize(delta: str) -> str using OpenAI chat completions format
  - Test: Test with mock API to verify correct request format

  Task 7: Implement Ollama provider class

  - Objective: Support locally-run Ollama models
  - Implementation: Create OllamaProvider class
  - Use Ollama's HTTP API (default: http://localhost:11434)
  - Implement summarize(delta: str) -> str using Ollama's generate endpoint
  - Test: Test with mock API to verify correct request format

  Task 8: Integration test and CLI flow

  - Objective: End-to-end testing of setup → summarize workflow
  - Implementation: Create test script that:
    1. Runs setup command with various inputs
    2. Runs summarize with configured model
    3. Verifies fallback to Gemini works

  - Test: Manual testing of all three flows (custom cloud API, local Ollama, Gemini fallback)
  - Demo: Show user setting up custom model, then summarize using it
