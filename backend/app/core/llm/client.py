"""LLM client for tarot interpretation using litellm.

Supports multiple providers (Ollama, xAI Grok, etc.) with unified interface.
Tracks usage metrics and costs to database for ops analysis.
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import litellm
import structlog
from litellm import acompletion

logger = structlog.get_logger(__name__)


@dataclass
class LLMResponse:
    """Response from LLM including content and usage metrics."""

    content: str
    model: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost_usd: float
    latency_ms: int

    def __str__(self) -> str:
        """Return the content for backwards compatibility."""
        return self.content


class UsageTracker(ABC):
    """Abstract base for tracking LLM usage to different backends."""

    @abstractmethod
    async def track(
        self,
        user_id: str | None,
        reading_id: str | None,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        latency_ms: int,
    ) -> None:
        """Track LLM usage metrics.

        Args:
            user_id: User making the request (optional)
            reading_id: Associated reading ID (optional)
            model: Model name
            provider: Provider name
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            cost_usd: Cost in USD
            latency_ms: Latency in milliseconds
        """
        pass


class DatabaseUsageTracker(UsageTracker):
    """Track usage to Supabase database for ops analysis."""

    def __init__(self, supabase_client: Any) -> None:
        """Initialize with Supabase client.

        Args:
            supabase_client: Initialized Supabase client
        """
        self.supabase = supabase_client

    async def track(
        self,
        user_id: str | None,
        reading_id: str | None,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        latency_ms: int,
    ) -> None:
        """Track usage to llm_usage table."""
        try:
            self.supabase.table("llm_usage").insert(
                {
                    "user_id": user_id,
                    "reading_id": reading_id,
                    "model": model,
                    "provider": provider,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                    "cost_usd": float(cost_usd),
                    "latency_ms": latency_ms,
                }
            ).execute()

            logger.info(
                "llm_usage_tracked",
                model=model,
                provider=provider,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=f"${cost_usd:.6f}",
                latency_ms=latency_ms,
                user_id=user_id,
                reading_id=reading_id,
            )
        except Exception as e:
            logger.error("failed_to_track_llm_usage", error=str(e))
            # Don't raise - usage tracking failure shouldn't break the reading


class LoggingUsageTracker(UsageTracker):
    """Track usage to structured logs only (for development)."""

    async def track(
        self,
        user_id: str | None,
        reading_id: str | None,
        model: str,
        provider: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        latency_ms: int,
    ) -> None:
        """Track usage to logs."""
        logger.info(
            "llm_usage_tracked",
            model=model,
            provider=provider,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            cost_usd=f"${cost_usd:.6f}",
            latency_ms=latency_ms,
            user_id=user_id,
            reading_id=reading_id,
        )


class LLMService:
    """Unified LLM service using litellm for provider abstraction."""

    def __init__(
        self,
        default_model: str,
        usage_tracker: UsageTracker | None = None,
    ) -> None:
        """Initialize LLM service.

        Args:
            default_model: Default model in litellm format (e.g., "ollama/neural-chat")
            usage_tracker: Optional tracker for usage metrics
        """
        self.default_model = default_model
        self.usage_tracker = usage_tracker or LoggingUsageTracker()

        # Configure litellm logging
        litellm.set_verbose = False

    def _extract_provider_and_model(self, model_string: str) -> tuple[str, str]:
        """Extract provider and model name from litellm format.

        Args:
            model_string: Format like "ollama/neural-chat" or "xai/grok-beta"

        Returns:
            Tuple of (provider, model_name)
        """
        if "/" in model_string:
            provider, model_name = model_string.split("/", 1)
            return provider, model_name
        return "unknown", model_string

    async def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: str | None = None,
        user_id: str | None = None,
        reading_id: str | None = None,
    ) -> LLMResponse:
        """Generate a completion from LLM.

        Args:
            system_prompt: System context for the model
            user_prompt: User's message/question
            model: Optional model override (in litellm format)
            user_id: Optional user ID for tracking
            reading_id: Optional reading ID for tracking

        Returns:
            LLMResponse: Model's response with usage metrics

        Raises:
            Exception: If the LLM call fails
        """
        model_to_use = model or self.default_model

        try:
            start_time = time.time()

            response = await acompletion(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.7,
                timeout=120,
            )

            latency_ms = int((time.time() - start_time) * 1000)

            # Extract content
            content = response.choices[0].message.content

            # Extract token usage
            usage = response.usage
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens

            # Calculate cost using litellm's built-in calculation
            cost_usd = litellm.completion_cost(response)

            # Extract provider and model name for tracking
            provider, model_name = self._extract_provider_and_model(model_to_use)

            # Track usage
            await self.usage_tracker.track(
                user_id=user_id,
                reading_id=reading_id,
                model=model_name,
                provider=provider,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                cost_usd=cost_usd,
                latency_ms=latency_ms,
            )

            llm_response = LLMResponse(
                content=str(content).strip(),
                model=model_to_use,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost_usd=cost_usd,
                latency_ms=latency_ms,
            )

            logger.info(
                "llm_generation_complete",
                model=model_to_use,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
                cost_usd=f"${cost_usd:.6f}",
                latency_ms=latency_ms,
            )

            return llm_response

        except Exception as e:
            logger.error(
                "llm_generation_failed",
                model=model_to_use,
                error=str(e),
            )
            raise


class LLMFactory:
    """Factory for creating LLM service with configuration."""

    _instance: LLMService | None = None

    @classmethod
    def create(
        cls,
        default_model: str = "xai/grok-4-1-fast-reasoning",
        usage_tracker: UsageTracker | None = None,
    ) -> LLMService:
        """Create an LLM service.

        Args:
            default_model: Default model in litellm format
            usage_tracker: Optional usage tracker

        Returns:
            LLMService: Configured service instance
        """
        return LLMService(default_model=default_model, usage_tracker=usage_tracker)

    @classmethod
    def get_instance(
        cls,
        default_model: str = "xai/grok-4-1-fast-reasoning",
        usage_tracker: UsageTracker | None = None,
    ) -> LLMService:
        """Get or create a singleton LLM service.

        Args:
            default_model: Default model in litellm format
            usage_tracker: Optional usage tracker

        Returns:
            LLMService: Singleton service instance
        """
        if cls._instance is None:
            cls._instance = cls.create(
                default_model=default_model,
                usage_tracker=usage_tracker,
            )
        return cls._instance
