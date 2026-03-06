"""
Base agent – shared LLM call logic for all ResearchPilot agents.
Supports Groq, OpenAI, OpenRouter, and Gemini providers.
"""
from typing import Optional
from config import get_settings

settings = get_settings()


class BaseAgent:
    def __init__(self, system_prompt: str = "", temperature: float = 0.3):
        self.system_prompt = system_prompt
        self.temperature = temperature

    async def _call_llm(self, user_message: str, max_tokens: int = 2048) -> str:
        """Call the configured LLM provider and return the text response."""
        if settings.is_demo:
            return self._demo_response(user_message)

        provider = settings.llm_provider.lower()

        if provider == "groq":
            return await self._call_groq(user_message, max_tokens)
        elif provider == "openai":
            return await self._call_openai(user_message, max_tokens)
        elif provider == "openrouter":
            return await self._call_openrouter(user_message, max_tokens)
        elif provider == "gemini":
            return await self._call_gemini(user_message, max_tokens)
        else:
            return await self._call_groq(user_message, max_tokens)

    def _build_messages(self, user_message: str) -> list:
        messages = []
        if self.system_prompt:
            messages.append({"role": "system", "content": self.system_prompt})
        messages.append({"role": "user", "content": user_message})
        return messages

    async def _call_groq(self, user_message: str, max_tokens: int) -> str:
        from groq import AsyncGroq
        client = AsyncGroq(api_key=settings.groq_api_key)
        response = await client.chat.completions.create(
            model=settings.llm_model,
            messages=self._build_messages(user_message),
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _call_openai(self, user_message: str, max_tokens: int) -> str:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self._build_messages(user_message),
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _call_openrouter(self, user_message: str, max_tokens: int) -> str:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        response = await client.chat.completions.create(
            model="meta-llama/llama-3.3-70b-instruct",
            messages=self._build_messages(user_message),
            temperature=self.temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or ""

    async def _call_gemini(self, user_message: str, max_tokens: int) -> str:
        import httpx
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash"
            f":generateContent?key={settings.google_api_key}"
        )
        payload = {
            "contents": [{"parts": [{"text": f"{self.system_prompt}\n\n{user_message}"}]}],
            "generationConfig": {"maxOutputTokens": max_tokens, "temperature": self.temperature},
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _demo_response(self, user_message: str) -> str:
        return (
            "[DEMO MODE] This is a placeholder response. "
            "Configure a valid API key (GROQ_API_KEY, OPENAI_API_KEY, etc.) "
            "in your .env file to enable real AI responses.\n\n"
            f"Agent: {self.__class__.__name__}\nInput: {user_message[:200]}..."
        )
