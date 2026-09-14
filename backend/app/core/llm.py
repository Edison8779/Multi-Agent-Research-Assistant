from typing import Type, TypeVar

from openai import AsyncOpenAI
from pydantic import BaseModel

from app.core.config import settings

T = TypeVar("T", bound=BaseModel)

# We use the AsyncOpenAI client
client = AsyncOpenAI(api_key=settings.LLM_API_KEY)


async def generate_text(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Generate a simple text response from the LLM.
    """
    response = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content or ""


async def generate_structured(
    prompt: str, response_model: Type[T], model: str = "gpt-4o-mini"
) -> T:
    """
    Generate a structured Pydantic output using OpenAI's parse API.
    """
    response = await client.beta.chat.completions.parse(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format=response_model,
    )

    parsed = response.choices[0].message.parsed
    if parsed is None:
        raise ValueError("Failed to parse the response into the structured model.")

    return parsed
