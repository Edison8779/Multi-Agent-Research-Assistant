from typing import Any

import httpx

from app.core.config import settings


async def search_web(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    """
    Search the web using the Tavily API. If the API key is invalid or missing,
    falls back to the free Wikipedia Search API.
    """
    # Use Tavily if a valid-looking key is provided
    if settings.SEARCH_API_KEY and settings.SEARCH_API_KEY.startswith("tvly-"):
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
            try:
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
            except Exception as e:
                print(f"Error fetching Tavily search results: {e}. Falling back to Wikipedia...")

    # Fallback to Wikipedia API
    wiki_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "utf8": "1",
        "format": "json",
        "srlimit": max_results,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Wikipedia API requires a User-Agent header
            headers = {"User-Agent": "MultiAgentResearchBot/1.0 (test@example.com)"}
            response = await client.get(wiki_url, params=params, headers=headers, timeout=15.0)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for r in data.get("query", {}).get("search", []):
                # Wikipedia returns a snippet with HTML tags, we should clean it slightly or just return it
                snippet = r.get("snippet", "").replace('<span class="searchmatch">', '').replace('</span>', '')
                title = r.get("title", "")
                results.append(
                    {
                        "title": title,
                        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
                        "snippet": snippet,
                    }
                )
            return results
        except Exception as e:
            print(f"Error fetching Wikipedia search results: {e}")
            return []
