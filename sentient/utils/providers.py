from abc import ABC, abstractmethod
from typing import Dict, Any
import os


class LLMProvider(ABC):
    @abstractmethod
    def get_client_config(self) -> Dict[str, str]:
        pass

class OpenAIProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": os.environ.get("OPENAI_API_KEY"),
            "base_url": "https://api.openai.com/v1",
        }

class TogetherAIProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": os.environ.get("TOGETHER_API_KEY"),
            "base_url": "https://api.together.xyz/v1",
        }

class OllamaProvider(LLMProvider):
    def get_client_config(self) -> Dict[str, str]:
        return {
            "api_key": "ollama",
            "base_url": "http://localhost:11434/v1/",
        }

# class AnyscaleProvider(LLMProvider):
#     def get_client_config(self) -> Dict[str, Any]:
#         return {
#             "api_key": os.environ.get("ANYSCALE_API_KEY"),
#             "base_url": "https://api.endpoints.anyscale.com/v1",
#         }

PROVIDER_MAP = {
    "openai": OpenAIProvider(),
    "together": TogetherAIProvider(),
    "ollama": OllamaProvider(),
    # "anyscale": AnyscaleProvider(),
}

def get_provider(provider_name: str) -> LLMProvider:
    provider = PROVIDER_MAP.get(provider_name.lower())
    if not provider:
        raise ValueError(f"Unsupported provider: {provider_name}. Choose one of the supported providers: {', '.join(PROVIDER_MAP.keys())}")
    return provider