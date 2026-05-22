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
        fallback_models: Optional[list] = None,
    ):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENROUTER_API_KEY")
        self.api_url = (
            api_url
            or os.getenv("DEEPSEEK_API_URL")
            or os.getenv("OPENROUTER_API_URL")
            or "https://openrouter.ai/api/v1"
        )
        self.model = os.getenv("MODEL_NAME") or model
        # Default fallback chain: primary model then the provided fallbacks
        if fallback_models is None:
            fallback_models = [
                "openai/gpt-oss-120b:free",
                "google/gemma-4-26b-a4b-it:free",
                "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free",
                "meta-llama/llama-3.3-70b-instruct:free",
                "qwen/qwen3-next-80b-a3b-instruct:free",
                "meta-llama/llama-3.2-3b-instruct:free",
            ]
        # Ensure primary model is first
        self.fallback_models = [self.model] + [m for m in fallback_models if m != self.model]
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
        # Helper to resolve api key + url for a given model/provider
        def _resolve_api_info(model_name: str):
            provider = model_name.split("/")[0].lower()
            # Map provider -> (env_api_key, env_api_url)
            mapping = {
                "deepseek": ("DEEPSEEK_API_KEY", "DEEPSEEK_API_URL"),
                "openrouter": ("OPENROUTER_API_KEY", "OPENROUTER_API_URL"),
                "openai": ("OPENAI_API_KEY", "OPENAI_API_URL"),
                "google": ("GOOGLE_API_KEY", "GOOGLE_API_URL"),
                "nvidia": ("NVIDIA_API_KEY", "NVIDIA_API_URL"),
            }
            key_env, url_env = mapping.get(provider, (None, None))
            key = os.getenv(key_env) if key_env else None
            url = os.getenv(url_env) if url_env else None
            # fallback to client-level values
            key = key or self.api_key
            url = url or self.api_url
            return key, url

        last_errors = []

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            # Try each model in the fallback chain once (no per-model retries)
            for model_try in self.fallback_models:
                key_try, url_try = _resolve_api_info(model_try)
                if not key_try:
                    logger.info("No API key available for model %s; skipping.", model_try)
                    last_errors.append((model_try, "missing_api_key"))
                    continue

                payload = {
                    "model": model_try,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }

                headers = {
                    "Authorization": f"Bearer {key_try}",
                    "Content-Type": "application/json",
                }
                if self.site_url:
                    headers["HTTP-Referer"] = self.site_url
                if self.site_name:
                    headers["X-Title"] = self.site_name

                base = url_try.rstrip("/")
                url = base + "/chat/completions"

                try:
                    resp = await client.post(url, json=payload, headers=headers)
                    text = await self._extract_text(resp)
                    if model_try != self.model:
                        logger.info("Model call succeeded with fallback model %s", model_try)
                    return text
                except Exception as exc:
                    logger.warning("Model %s call failed: %s", model_try, exc)
                    last_errors.append((model_try, str(exc)))
                    # move on to next model without retrying

        # If we reach here, all models failed
        tried = ", ".join([m for m, _ in last_errors])
        raise ClaudeClientError(f"All model attempts failed ({tried}). Last errors: {last_errors}")

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
