import pytest
import respx
import httpx

from app.core.config import settings
from app.tools.web_search import search_web


@pytest.mark.asyncio
@respx.mock
async def test_search_web_success():
    # Ensure API key is set for testing
    settings.SEARCH_API_KEY = "dummy_key"
    
    mock_response = {
        "results": [
            {
                "title": "Mock Title 1",
                "url": "https://example.com/1",
                "content": "Mock snippet 1",
            },
            {
                "title": "Mock Title 2",
                "url": "https://example.com/2",
                "content": "Mock snippet 2",
            }
        ]
    }
    
    respx.post("https://api.tavily.com/search").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    results = await search_web("test query")
    
    assert len(results) == 2
    assert results[0]["title"] == "Mock Title 1"
    assert results[0]["url"] == "https://example.com/1"
    assert results[0]["snippet"] == "Mock snippet 1"


@pytest.mark.asyncio
@respx.mock
async def test_search_web_error():
    settings.SEARCH_API_KEY = "dummy_key"
    
    respx.post("https://api.tavily.com/search").mock(
        return_value=httpx.Response(500)
    )

    results = await search_web("test query")
    assert results == []
