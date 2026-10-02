"""Groq LLM adapter for CrewAI 1.x built on langchain-groq.

CrewAI 1.x no longer accepts LangChain chat models directly, and routing
"groq/..." model strings requires the optional LiteLLM package. This adapter
exposes LangChain's ChatGroq through CrewAI's BaseLLM interface, so the
project only needs `crewai` and `langchain-groq`.
"""
from __future__ import annotations

from typing import Any

from crewai import BaseLLM
from langchain_groq import ChatGroq
from pydantic import PrivateAttr

DEFAULT_MODEL = "llama-3.3-70b-versatile"
AVAILABLE_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.1-8b-instant",
    "openai/gpt-oss-120b",
]


def _to_lc_messages(messages: str | list[dict[str, Any]]) -> list[tuple[str, str]]:
    """Convert CrewAI messages into (role, content) tuples for LangChain."""
    if isinstance(messages, str):
        return [("user", messages)]
    role_map = {"system": "system", "user": "user", "assistant": "assistant"}
    converted: list[tuple[str, str]] = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):  # multimodal blocks -> plain text
            content = "\n".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            )
        converted.append((role_map.get(msg.get("role", "user"), "user"), str(content)))
    return converted


class GroqChatLLM(BaseLLM):
    """CrewAI-compatible LLM that delegates to langchain_groq.ChatGroq."""

    llm_type: str = "groq-langchain"
    provider: str = "groq"
    _client: Any = PrivateAttr(default=None)

    def __init__(self, api_key: str, model: str = DEFAULT_MODEL,
                 temperature: float = 0.2, max_tokens: int = 4096,
                 client: Any = None, **kwargs: Any) -> None:
        super().__init__(model=model, api_key=api_key, temperature=temperature,
                         max_tokens=max_tokens, **kwargs)
        self._client = client or ChatGroq(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            max_retries=3,
            timeout=120,
        )

    def call(self, messages, tools=None, callbacks=None, available_functions=None,
             from_task=None, from_agent=None, response_model=None) -> str:
        response = self._client.invoke(_to_lc_messages(messages))
        content = response.content
        if isinstance(content, list):
            content = "".join(
                c.get("text", "") if isinstance(c, dict) else str(c) for c in content
            )
        text = str(content).strip()
        # CrewAI's text-mode parser expects a "Final Answer:" marker. Llama-style
        # models sometimes answer directly; no tools are used here, so wrap it.
        if "Final Answer:" not in text and "Action:" not in text:
            text = f"Thought: I now know the final answer\nFinal Answer: {text}"
        return text

    def supports_function_calling(self) -> bool:
        return False

    def supports_stop_words(self) -> bool:
        return True

    def get_context_window_size(self) -> int:
        return 100000
