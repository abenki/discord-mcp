"""Configuration validation utilities."""
import os
import requests


class ConfigValidator:
    """Validates bot configuration and external service connectivity."""

    @staticmethod
    def validate_environment():
        """Validate all required environment variables and configurations."""
        print("🔍 Validating configuration...")

        # Check Discord token
        discord_token = os.getenv("DISCORD_BOT_TOKEN")
        if not discord_token:
            raise ValueError(
                "❌ DISCORD_BOT_TOKEN environment variable is required!")
        print("✅ Discord bot token found")

        # Check Ollama configuration
        ollama_url = os.getenv(
            "OLLAMA_API_URL", "http://localhost:11434/api/generate")
        ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:14b")

        print(f"🔧 Ollama API URL: {ollama_url}")
        print(f"🤖 Ollama Model: {ollama_model}")

        # Test Ollama connectivity
        ConfigValidator._test_ollama_connection(ollama_url, ollama_model)

        print("✅ Configuration validation complete!")
        return True

    @staticmethod
    def _test_ollama_connection(api_url, model_name):
        """Test connection to Ollama API."""
        print("🔌 Testing Ollama connection...")

        try:
            # Extract base URL for health check
            base_url = api_url.replace("/api/generate", "")

            # Test basic connectivity
            health_response = requests.get(f"{base_url}/api/tags", timeout=5)
            if health_response.status_code != 200:
                raise ConnectionError(f"Ollama server not responding (status: {
                                      health_response.status_code})")

            # Check if the specified model is available
            available_models = health_response.json().get("models", [])
            model_names = [model.get("name", "") for model in available_models]

            if model_name not in model_names:
                print(f"⚠️  Model '{
                      model_name}' not found in available models:")
                for model in model_names[:5]:  # Show first 5 models
                    print(f"   - {model}")
                if len(model_names) > 5:
                    print(f"   ... and {len(model_names) - 5} more models")
                print(f"\n💡 To pull the model, run: ollama pull {model_name}")
                print("   Or set OLLAMA_MODEL to an available model in your .env file")
                raise ValueError(f"Model '{model_name}' not available")

            print(f"✅ Ollama connection successful, model '{
                  model_name}' available")

        except requests.exceptions.ConnectionError:
            print(f"❌ Cannot connect to Ollama at {api_url}")
            print("💡 Make sure Ollama is running:")
            print("   - Install: brew install ollama (macOS) or visit https://ollama.com")
            print("   - Start: ollama serve")
            print(f"   - Pull model: ollama pull {model_name}")
            raise ConnectionError("Ollama server not accessible")
        except requests.exceptions.Timeout:
            print(f"❌ Timeout connecting to Ollama at {api_url}")
            raise ConnectionError("Ollama server timeout")
        except Exception as e:
            print(f"❌ Error testing Ollama connection: {e}")
            raise
