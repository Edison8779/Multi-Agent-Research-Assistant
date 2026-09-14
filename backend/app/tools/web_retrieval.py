from typing import Any

import httpx
from bs4 import BeautifulSoup


async def fetch_page(url: str) -> dict[str, Any]:
    """
    Fetch a web page and clean its HTML content to return plain text.
    Handles basic timeouts and errors.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        async with httpx.AsyncClient(follow_redirects=True) as client:
            response = await client.get(url, headers=headers, timeout=15.0)
            response.raise_for_status()

            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            # Remove scripts, styles, and other non-content tags
            for element in soup(
                ["script", "style", "nav", "footer", "header", "noscript"]
            ):
                element.decompose()

            title = soup.title.string if soup.title else ""

            # Extract text and collapse whitespace
            text = soup.get_text(separator=" ")
            clean_text = " ".join(text.split())

            return {
                "title": title.strip(),
                "url": url,
                "content": clean_text,
                "error": None,
            }

    except Exception as e:
        return {"title": "", "url": url, "content": "", "error": str(e)}
