"""Groq LLM adapter for CrewAI 1.x built on langchain-groq.

CrewAI 1.x no longer accepts LangChain chat models directly, so this adapter
exposes LangChain's ChatGroq through CrewAI's BaseLLM interface.
"""

from __future__ import annotations

from typing import Any

from crewai import BaseLLM
from langchain_groq import ChatGroq
from pydantic import PrivateAttr


# Keep the default model inside AVAILABLE_MODELS.
DEFAULT_MODEL = "llama-3.1-8b-instant"

AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
]


def _to_lc_messages(
    messages: str | list[dict[str, Any]]
) -> list[tuple[str, str]]:
    """Convert CrewAI messages into LangChain message tuples."""

    if isinstance(messages, str):
        return [("user", messages)]

    role_map = {
        "system": "system",
        "user": "user",
        "assistant": "assistant",
    }

    converted: list[tuple[str, str]] = []

    for msg in messages:
        content = msg.get("content", "")

        # Handle multimodal/content blocks safely.
        if isinstance(content, list):
            text_parts = []

            for part in content:
                if isinstance(part, dict):
                    text_parts.append(str(part.get("text", "")))
                else:
                    text_parts.append(str(part))

            content = "\n".join(text_parts)

        role = role_map.get(msg.get("role", "user"), "user")
        converted.append((role, str(content)))

    return converted


class GroqChatLLM(BaseLLM):
    """CrewAI-compatible LLM using LangChain's ChatGroq."""

    llm_type: str = "groq-langchain"
    provider: str = "groq"

    _client: Any = PrivateAttr(default=None)

    def __init__(
        self,
        api_key: str,
        model: str = DEFAULT_MODEL,
        temperature: float = 0.2,
        max_tokens: int = 4096,
        client: Any = None,
        **kwargs: Any,
    ) -> None:

        # Safety fallback:
        # If an invalid/empty model is supplied, use DEFAULT_MODEL.
        if not model or model not in AVAILABLE_MODELS:
            model = DEFAULT_MODEL

        super().__init__(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs,
        )

        self._client = client or ChatGroq(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=3,
            timeout=120,
        )

    def call(
        self,
        messages,
        tools=None,
        callbacks=None,
        available_functions=None,
        from_task=None,
        from_agent=None,
        response_model=None,
    ) -> str:

        response = self._client.invoke(
            _to_lc_messages(messages)
        )

        content = response.content

        # Some LangChain responses may return structured content.
        if isinstance(content, list):
            content = "".join(
                c.get("text", "") if isinstance(c, dict) else str(c)
                for c in content
            )

        text = str(content).strip()

        # CrewAI text parser compatibility.
        if (
            "Final Answer:" not in text
            and "Action:" not in text
        ):
            text = (
                "Thought: I now know the final answer\n"
                f"Final Answer: {text}"
            )

        return text

    def supports_function_calling(self) -> bool:
        return False

    def supports_stop_words(self) -> bool:
        return True

    def get_context_window_size(self) -> int:
        return 100000
