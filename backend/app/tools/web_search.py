from typing import Any

import httpx

from app.core.config import settings


async def search_web(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """
    Search the web using the Tavily API (or alternative Search API).
    Expects SEARCH_API_KEY to be set in the environment.
    """
    if not settings.SEARCH_API_KEY:
        # Fallback or stub if no key is provided during testing
        return [
            {
                "title": "Example Search Result",
                "url": "https://example.com",
                "snippet": "Example snippet for query: " + query,
            }
        ]

    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": settings.SEARCH_API_KEY,
        "query": query,
        "max_results": max_results,
        "include_answer": False,
        "include_raw_content": False,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=15.0)
        response.raise_for_status()
        data = response.json()

        results = []
        for r in data.get("results", []):
            results.append(
                {
                    "title": r.get("title", ""),
                    "url": r.get("url", ""),
                    "snippet": r.get("content", ""),
                }
            )

        return results
