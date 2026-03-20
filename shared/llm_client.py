import os
import aiohttp
import asyncio
import json
from typing import List, Dict, Any, Optional
from .config import Config

class LLMClient:
    """Chutes-only LLM client with timeout and retry."""

    def __init__(self, provider: str = "chutes", max_retries: int = 3):
        self.provider = provider
        self.session: Optional[aiohttp.ClientSession] = None
        self.max_retries = max_retries
        self.timeout = aiohttp.ClientTimeout(total=60)

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        system_prompt: Optional[str] = None
    ) -> str:
        """Send chat request to Chutes API with retry."""
        api_key = Config.CHUTES_API_KEY
        if not api_key:
            raise ValueError("CHUTES_API_KEY not set")

        url = "https://llm.chutes.ai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        chat_messages = []
        if system_prompt:
            chat_messages.append({"role": "system", "content": system_prompt})
        chat_messages.extend(messages)

        model_name = model or Config.DEFAULT_MODEL

        payload = {
            "model": model_name,
            "messages": chat_messages,
            "max_tokens": 2000
        }

        last_error = None
        for attempt in range(1, self.max_retries + 1):
            try:
                async with self.session.post(url, headers=headers, json=payload) as resp:
                    text = await resp.text()
                    if resp.status != 200:
                        raise Exception(f"Chutes API error {resp.status}: {text[:200]}")

                    data = json.loads(text)
                    content = data["choices"][0]["message"].get("content")
                    if content is None:
                        print(f"[WARN] Model returned None - possible refusal. Full: {text[:300]}")
                        return "..."
                    return content.strip()

            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_error = e
                if attempt < self.max_retries:
                    wait = 2 ** (attempt - 1)
                    print(f"[RETRY] Chutes request failed (attempt {attempt}/{self.max_retries}): {e}. Waiting {wait}s...")
                    await asyncio.sleep(wait)
                    continue
                raise Exception(f"Chutes API failed after {self.max_retries} attempts: {last_error}") from last_error