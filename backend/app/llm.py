"""
=========================================================
llm.py

LLM Service for StadiumOS AI.

Responsibilities
----------------
- Connect to OpenRouter
- Generate AI responses
- Return structured JSON
- Handle retries
- Keep AI provider isolated

=========================================================
"""

from __future__ import annotations

import json

import httpx

from app.config import logger, settings


class LLMService:
    """
    Wrapper around OpenRouter.
    """

    BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

    MODEL_ROUTING = {
        "prediction": settings.DEFAULT_MODEL,
        "incident": settings.DEFAULT_MODEL,
        "volunteer": settings.DEFAULT_MODEL,
        "summary": settings.DEFAULT_MODEL,
    }

    def __init__(self):

        self.client = httpx.Client(timeout=30)
        self.api_key = settings.OPENROUTER_API_KEY.strip()
        if not self.api_key:
            logger.warning("OPENROUTER_API_KEY is not set in environment. LLM features will fall back to local heuristics.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:8000",
            "X-Title": "StadiumOS AI",
        }

    # =====================================================
    # Internal Request
    # =====================================================

    def _request(
        self,
        prompt: str,
        task: str = "prediction",
    ) -> str:

        if not self.api_key:
            raise RuntimeError("OPENROUTER_API_KEY is not set in environment variables.")

        payload = {
        "model": self.MODEL_ROUTING.get(
            task,
            settings.DEFAULT_MODEL,
        ),
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": settings.MODEL_TEMPERATURE,
        "max_tokens": settings.MAX_OUTPUT_TOKENS,
        "response_format": {
            "type": "json_object"
        },
        }

        response = self.client.post(
            self.BASE_URL,
            headers=self.headers,
            json=payload,
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]

    # =====================================================
    # Public API
    # =====================================================

    def generate(
        self,
        prompt: str,
        task: str = "prediction",
    ) -> str:

        try:

            return self._request(prompt, task)

        except Exception as e:

            logger.exception("LLM request failed.")

            raise RuntimeError(str(e))

    def generate_json(
        self,
        prompt: str,
        task: str = "prediction",
    ) -> dict:

        try:
            response = self.generate(prompt, task)
        except RuntimeError as exc:
            logger.exception("LLM generate_json failed.")
            return {
                "error": "LLM request failed",
                "details": str(exc),
            }

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            logger.exception("Invalid JSON received from LLM.")
            return {
                "error": "Invalid JSON",
                "raw": response,
            }

    def health(self) -> bool:

        try:

            self.generate(
                "Reply only with OK.",
                task="summary",
            )

            return True

        except Exception:

            return False


llm = LLMService()