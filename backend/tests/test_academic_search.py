import pytest
import respx
import httpx

from app.tools.academic_search import search_papers


@pytest.mark.asyncio
@respx.mock
async def test_search_papers_success():
    mock_response = {
        "data": [
            {
                "title": "A Great Paper",
                "authors": [{"name": "John Doe"}, {"name": "Jane Smith"}],
                "abstract": "This is a great paper.",
                "year": 2026,
                "url": "https://example.com/paper1",
                "externalIds": {"DOI": "10.1234/5678"}
            }
        ]
    }
    
    respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
        return_value=httpx.Response(200, json=mock_response)
    )

    results = await search_papers("test query")
    
    assert len(results) == 1
    assert results[0]["title"] == "A Great Paper"
    assert results[0]["authors"] == ["John Doe", "Jane Smith"]
    assert results[0]["abstract"] == "This is a great paper."
    assert results[0]["year"] == 2026
    assert results[0]["paper_url"] == "https://example.com/paper1"
    assert results[0]["doi"] == "10.1234/5678"


@pytest.mark.asyncio
@respx.mock
async def test_search_papers_error():
    respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
        return_value=httpx.Response(500)
    )

    results = await search_papers("test query")
    assert results == []
