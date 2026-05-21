import os
import asyncio
import logging
from typing import Any, Dict, Optional

import httpx
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def _compact_error_text(body: str, limit: int = 320) -> str:
    if not isinstance(body, str):
        return "<non-text error body>"
    compact = " ".join(body.split())
    if len(compact) <= limit:
        return compact
    return compact[:limit] + "..."


class ClaudeClientError(Exception):
    pass


class ClaudeClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_url: Optional[str] = None,
        model: str = "deepseek/deepseek-v4-flash:free",
        timeout: int = 10,
        max_retries: int = 3,
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.api_url = (
            api_url
            or os.getenv("DEEPSEEK_API_URL")
            or os.getenv("OPENROUTER_API_URL")
            or "https://openrouter.ai/api/v1"
        )
        self.model = os.getenv("MODEL_NAME") or model
        self.timeout = timeout
        self.max_retries = max_retries
        self.site_url = os.getenv("SITE_URL")
        self.site_name = os.getenv("SITE_NAME")

        if not self.api_key:
            logger.warning("No DEEPSEEK_API_KEY/OPENROUTER_API_KEY found in environment; client will fail on send.")

    async def send_prompt(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        max_tokens: int = 1000,
    ) -> str:
        """Send prompts to the configured model API and return the raw text output.

        This wrapper implements retry/backoff and tolerates several response formats.
        """
        if not self.api_key:
            raise ClaudeClientError("Missing DEEPSEEK_API_KEY or OPENROUTER_API_KEY environment variable")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if self.site_url:
            headers["HTTP-Referer"] = self.site_url
        if self.site_name:
            headers["X-Title"] = self.site_name

        base = self.api_url.rstrip("/")
        if base.endswith("/api/v1"):
            url = base + "/chat/completions"
        elif base.endswith("/v1"):
            url = base + "/chat/completions"
        else:
            url = base + "/chat/completions"

        backoff_base = 0.5

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            last_exc = None
            for attempt in range(1, self.max_retries + 1):
                try:
                    resp = await client.post(url, json=payload, headers=headers)
                    text = await self._extract_text(resp)
                    return text
                except Exception as exc:
                    last_exc = exc
                    logger.warning("Model call attempt %s failed: %s", attempt, exc)
                    if attempt == self.max_retries:
                        break
                    sleep_for = backoff_base * (2 ** (attempt - 1))
                    await asyncio.sleep(sleep_for)

        raise ClaudeClientError(f"Model API call failed after {self.max_retries} attempts: {last_exc}")

    async def _extract_text(self, resp: httpx.Response) -> str:
        status = resp.status_code
        if status >= 500:
            raise ClaudeClientError(f"Model API server error: {status}")
        if status >= 400:
            # surface the body for debugging
            body = resp.text
            raise ClaudeClientError(f"Model API returned {status}: {_compact_error_text(body)}")

        # Try to parse JSON and extract likely text fields
        try:
            j = resp.json()
        except Exception:
            return resp.text

        # Common patterns: 'choices', 'completion', 'output', 'text', 'result'.
        if isinstance(j, dict):
            if "choices" in j and isinstance(j["choices"], list):
                parts = []
                for c in j["choices"]:
                    if isinstance(c, dict):
                        # OpenAI/OpenRouter style
                        msg = c.get("message")
                        if isinstance(msg, dict):
                            content = msg.get("content")
                            if isinstance(content, str):
                                parts.append(content)
                            elif isinstance(content, list):
                                for item in content:
                                    if isinstance(item, dict) and item.get("type") == "text" and isinstance(item.get("text"), str):
                                        parts.append(item["text"])
                        # Some providers return direct text
                        if isinstance(c.get("text"), str):
                            parts.append(c["text"])
                if parts:
                    return "\n".join(parts)

            if "completion" in j:
                return j["completion"]
            if "output" in j:
                return j["output"]
            if "text" in j:
                return j["text"]
            if "result" in j:
                return j["result"]

        # Fallback: return the raw response text
        return resp.text
