import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(async_client: AsyncClient) -> None:
    response = await async_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Backend is running"}


@pytest.mark.asyncio
async def test_research_single_endpoint_success(async_client: AsyncClient) -> None:
    mock_result = {
        "question": "What is Python?",
        "search_queries": ["What is Python?"],
        "search_results": [{"title": "Python", "url": "https://python.org", "snippet": "A language"}],
        "retrieved_documents": [{"title": "Python", "url": "https://python.org", "content": "Python is dynamic."}],
        "findings": [{
            "claim": "Python is dynamic",
            "evidence": "Python is dynamic.",
            "source_url": "https://python.org",
            "source_title": "Python",
            "confidence": 0.95
        }],
        "final_answer": "Python is a dynamic programming language."
    }

    mock_agent = AsyncMock()
    mock_agent.ainvoke.return_value = mock_result

    with patch("app.api.v1.endpoints.research.get_agent", return_value=mock_agent):
        response = await async_client.post(
            "/api/v1/research/single",
            json={"question": "What is Python?"}
        )

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "What is Python?"
    assert len(data["findings"]) == 1
    assert data["findings"][0]["claim"] == "Python is dynamic"
    assert data["final_answer"] == "Python is a dynamic programming language."
