"""
Core processing module for analyzing and summarizing text notes.
Includes performance benchmarking (latency and tokens/sec calculation).
"""

import time
from typing import Any, Dict
from openai import OpenAI
from config import get_client_config


def process_text_summarization(text: str, use_remote: bool = False) -> Dict[str, Any]:
    """
    Processes the input text and generates a concise summary along with execution benchmarks.

    :param text: Raw note or document string to summarize.
    :param use_remote: Flag indicating whether to use local or remote LLM.
    :return: Dictionary containing the summary output and key benchmarking metrics.
    """
    config = get_client_config(use_remote=use_remote)
    client = OpenAI(base_url=config.base_url, api_key=config.api_key)

    system_prompt = (
        "You are an offline-first, privacy-conscious AI assistant. "
        "Summarize the provided text into clean, structured, and actionable bullet points."
    )

    start_time = time.time()

    response = client.chat.completions.create(
        model=config.model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text},
        ],
        temperature=0.3,
    )

    elapsed_time = time.time() - start_time
    output_text = response.choices[0].message.content or ""

    # Estimate token count (standard heuristic: 1 word ~ 1.33 tokens)
    estimated_tokens = len(output_text.split()) * 1.33
    tokens_per_sec = estimated_tokens / elapsed_time if elapsed_time > 0 else 0.0

    return {
        "summary": output_text,
        "model": config.model_name,
        "mode": "Remote (OpenAI)" if use_remote else "Local (Ollama)",
        "elapsed_time": round(elapsed_time, 2),
        "tokens_per_sec": round(tokens_per_sec, 2),
    }