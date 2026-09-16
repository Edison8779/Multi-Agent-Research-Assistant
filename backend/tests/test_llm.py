import pytest
from pydantic import BaseModel

from app.core.config import settings
from app.core.llm import (
    generate_text,
    generate_structured,
    generate_stream,
    calculate_cost,
    TokenUsage,
)

requires_api_key = pytest.mark.skipif(
    not settings.LLM_API_KEY or settings.LLM_API_KEY == "dummy_key_to_allow_import",
    reason="LLM_API_KEY is not set",
)


class ResearchPlan(BaseModel):
    objective: str
    tasks: list[str]


@pytest.mark.asyncio
async def test_calculate_cost():
    cost = calculate_cost(settings.LLM_MODEL, 1000, 2000)
    # Default is llama3.1 which is free, so cost should be 0.0. 
    # (Or it will match whatever model is in settings)
    if settings.LLM_MODEL == "llama-3.1-8b-instant":
        assert abs(cost - 0.0) < 1e-6
    else:
        assert cost >= 0.0


@requires_api_key
@pytest.mark.asyncio
async def test_generate_text():
    response = await generate_text(
        prompt="Say hello!",
        system_message="You are a helpful assistant.",
        temperature=0.0
    )
    assert response.content
    assert isinstance(response.usage, TokenUsage)
    assert response.usage.total_tokens > 0


@requires_api_key
@pytest.mark.asyncio
async def test_generate_structured():
    plan, usage = await generate_structured(
        prompt="I want to research the history of artificial intelligence.",
        response_model=ResearchPlan,
        system_message="You are a research planner.",
    )
    assert isinstance(plan, ResearchPlan)
    assert isinstance(plan.objective, str)
    assert len(plan.tasks) > 0
    assert isinstance(usage, TokenUsage)
    assert usage.total_tokens > 0


@requires_api_key
@pytest.mark.asyncio
async def test_generate_stream():
    chunks = []
    async for chunk in generate_stream("Count to 3.", temperature=0.0):
        chunks.append(chunk)
    
    full_text = "".join(chunks)
    assert "1" in full_text
    assert "2" in full_text
    assert "3" in full_text
