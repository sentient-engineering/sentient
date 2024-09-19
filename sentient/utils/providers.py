from abc import ABC, abstractmethod
from typing import Dict, Any
import os


class LLMProvider(ABC):
    @abstractmethod
    def get_client_config(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        pass

class OpenAIProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "base_url": "https://api.openai.com/v1",
        }
    def get_provider_name(self) -> str:
        return "openai"

class TogetherAIProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": os.environ.get("TOGETHER_API_KEY"),
            "base_url": "https://api.together.xyz/v1",
        } 
    def get_provider_name(self) -> str:
        return "together"

class OllamaProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": "ollama",
            "base_url": "http://localhost:11434/v1/",
        }
    def get_provider_name(self) -> str:
        return "ollama"

class GroqProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": os.environ.get("GROQ_API_KEY"),
        }
    def get_provider_name(self) -> str:
        return "groq"
    
class AnthropicProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": os.environ.get("ANTHROPIC_API_KEY"),
        }
    def get_provider_name(self) -> str:
            return "anthropic"

class CustomProvider(LLMProvider):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_client_config(self) -> Dict[str, Any]:
        return {
            "api_key": os.environ.get("CUSTOM_API_KEY"),
            "base_url": self.base_url,
        }
    
    def get_provider_name(self) -> str:
            return "custom"
    
# class GoogleProvider(LLMProvider):
#     def get_client_config(self) -> Dict[str, str]:
#         api_key = os.environ.get("GOOGLE_API_KEY")
#         os.environ['API_KEY'] = api_key
#         return {
#             "api_key": os.environ.get("GOOGLE_API_KEY"),
#         }
#     def get_provider_name(self) -> str:
#         return "google"

PROVIDER_MAP = {
    "openai": OpenAIProvider(),
    "together": TogetherAIProvider(),
    "ollama": OllamaProvider(),
    "groq": GroqProvider(),
    "anthropic": AnthropicProvider(),
    # "google": GoogleProvider(),
}

def get_provider(provider_name: str, custom_base_url: str = None) -> LLMProvider:
    if provider_name.lower() == "custom":
        if not custom_base_url:
            raise ValueError("Custom provider requires a base_url")
        return CustomProvider(custom_base_url)
    else:
        provider = PROVIDER_MAP.get(provider_name.lower())
        if not provider:
            raise ValueError(f"Unsupported provider: {provider_name}. Choose one of the supported providers: {', '.join(PROVIDER_MAP.keys())}")
        return provider