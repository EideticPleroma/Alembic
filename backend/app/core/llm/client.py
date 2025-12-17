"""LLM client for tarot interpretation.

Supports both local (Ollama) and cloud (Grok) providers.
"""

from abc import ABC, abstractmethod

import httpx
import structlog

logger = structlog.get_logger(__name__)


class LLMClient(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate a completion from the LLM.

        Args:
            system_prompt: System context for the model
            user_prompt: User's message/question

        Returns:
            str: Model's response

        Raises:
            Exception: If the LLM call fails
        """
        pass


class OllamaClient(LLMClient):
    """Client for local Ollama models.

    Uses the Ollama API running locally (default: http://localhost:11434).
    """

    def __init__(
        self, base_url: str = "http://localhost:11434", model: str = "neural-chat"
    ):
        """Initialize Ollama client.

        Args:
            base_url: Base URL of Ollama API
            model: Model name to use (must be pulled in Ollama)
        """
        self.base_url = base_url
        self.model = model
        self.client = httpx.AsyncClient(timeout=120.0)

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using Ollama.

        Args:
            system_prompt: System context
            user_prompt: User message

        Returns:
            str: Model response
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": user_prompt,
                    "system": system_prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
            )
            response.raise_for_status()

            result = response.json()
            response_text = result.get("response", "")
            return str(response_text).strip()

        except Exception as e:
            logger.error("ollama_error", error=str(e), model=self.model)
            raise

    async def check_health(self) -> bool:
        """Check if Ollama is running and model is available.

        Returns:
            bool: True if healthy, False otherwise
        """
        try:
            response = await self.client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                tags = response.json().get("models", [])
                model_names = [m.get("name", "").split(":")[0] for m in tags]
                return self.model in model_names
            return False
        except Exception:
            return False

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()


class GrokClient(LLMClient):
    """Client for xAI Grok API.

    Production LLM provider. Requires XAI_API_KEY environment variable.
    """

    def __init__(self, api_key: str):
        """Initialize Grok client.

        Args:
            api_key: xAI API key
        """
        self.api_key = api_key
        self.base_url = "https://api.x.ai/v1"
        self.model = "grok-beta"
        self.client = httpx.AsyncClient(timeout=60.0)

    async def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate response using Grok API.

        Args:
            system_prompt: System context
            user_prompt: User message

        Returns:
            str: Model response
        """
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024,
                },
            )
            response.raise_for_status()

            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return str(content).strip()

        except Exception as e:
            logger.error("grok_error", error=str(e))
            raise

    async def close(self) -> None:
        """Close the HTTP client."""
        await self.client.aclose()


class LLMFactory:
    """Factory for creating LLM clients based on configuration."""

    _instance: LLMClient | None = None

    @classmethod
    def create(
        cls,
        use_local: bool = True,
        ollama_base_url: str = "http://localhost:11434",
        grok_api_key: str | None = None,
    ) -> LLMClient:
        """Create an LLM client.

        Args:
            use_local: Use local Ollama if True, Grok if False
            ollama_base_url: Base URL for Ollama
            grok_api_key: API key for Grok

        Returns:
            LLMClient: Configured client instance
        """
        if use_local:
            return OllamaClient(base_url=ollama_base_url)
        elif grok_api_key:
            return GrokClient(api_key=grok_api_key)
        else:
            msg = "Grok requires XAI_API_KEY"
            raise ValueError(msg)

    @classmethod
    def get_instance(
        cls,
        use_local: bool = True,
        ollama_base_url: str = "http://localhost:11434",
        grok_api_key: str | None = None,
    ) -> LLMClient:
        """Get or create a singleton LLM client.

        Args:
            use_local: Use local Ollama if True
            ollama_base_url: Base URL for Ollama
            grok_api_key: API key for Grok

        Returns:
            LLMClient: Singleton client instance
        """
        if cls._instance is None:
            cls._instance = cls.create(use_local, ollama_base_url, grok_api_key)
        return cls._instance
