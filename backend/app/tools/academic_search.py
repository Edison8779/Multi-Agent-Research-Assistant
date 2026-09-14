from typing import Any

import httpx


async def search_papers(query: str, limit: int = 5) -> list[dict[str, Any]]:
    """
    Search for academic papers using the Semantic Scholar Graph API.
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        "query": query,
        "limit": limit,
        "fields": "title,authors,abstract,year,url,externalIds",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()

            results = []
            for paper in data.get("data", []):
                authors = [
                    a.get("name") for a in paper.get("authors", []) if a.get("name")
                ]

                # Extract DOI if available
                doi = paper.get("externalIds", {}).get("DOI", "")

                results.append(
                    {
                        "title": paper.get("title", ""),
                        "authors": authors,
                        "abstract": paper.get("abstract", ""),
                        "year": paper.get("year"),
                        "paper_url": paper.get("url", ""),
                        "doi": doi,
                    }
                )

            return results

        except Exception as e:
            # Depending on error handling strategy, we can log and return [] or raise
            print(f"Error fetching papers: {e}")
            return []
