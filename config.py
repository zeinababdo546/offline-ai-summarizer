"""
Configuration module for Offline-First AI Note Summarizer.
Handles switching between local Ollama server and hosted OpenAI / OpenRouter APIs.
"""

import os
from typing import NamedTuple


class ClientConfig(NamedTuple):
    base_url: str | None
    api_key: str
    model_name: str


def get_client_config(use_remote: bool = False) -> ClientConfig:
    """
    Returns API client configuration based on execution context.

    :param use_remote: If True, uses cloud endpoint (OpenRouter or OpenAI). If False, uses local Ollama.
    :return: ClientConfig named tuple containing base_url, api_key, and model_name.
    """
    if use_remote:
        api_key = os.getenv("OPENAI_API_KEY", "").strip()
        if not api_key:
            raise ValueError(
                "Missing API Key: Please set the 'OPENAI_API_KEY' environment variable to use remote mode."
            )
        
        # Check if the key belongs to OpenRouter
        if api_key.startswith("sk-or-v1"):
            return ClientConfig(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key,
                model_name="openai/gpt-4o-mini",  # Formatted for OpenRouter
            )
            
        # Default standard OpenAI setup
        return ClientConfig(
            base_url=None,  # Defaults to standard OpenAI API URL
            api_key=api_key,
            model_name="gpt-4o-mini",
        )

    # Local Ollama endpoint setup (OpenAI-compatible)
    return ClientConfig(
        base_url="http://localhost:11434/v1",
        api_key="ollama",  # Dummy key required by OpenAI client SDK
        model_name="qwen2.5:3b",
    )