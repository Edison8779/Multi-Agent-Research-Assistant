import pytest
import respx
import httpx

from app.tools.web_retrieval import fetch_page


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_success():
    html_content = """
    <html>
        <head><title>Test Page</title></head>
        <body>
            <header>Header</header>
            <nav>Nav</nav>
            <main>
                <h1>Main Content</h1>
                <p>This is the text we want.</p>
            </main>
            <script>console.log("script")</script>
            <style>body { color: red; }</style>
            <footer>Footer</footer>
        </body>
    </html>
    """
    
    respx.get("https://example.com").mock(
        return_value=httpx.Response(200, text=html_content)
    )

    result = await fetch_page("https://example.com")
    
    assert result["title"] == "Test Page"
    assert result["url"] == "https://example.com"
    assert "This is the text we want." in result["content"]
    assert "Main Content" in result["content"]
    assert "Header" not in result["content"]
    assert "Footer" not in result["content"]
    assert "console.log" not in result["content"]
    assert result["error"] is None


@pytest.mark.asyncio
@respx.mock
async def test_fetch_page_error():
    respx.get("https://example.com").mock(
        return_value=httpx.Response(404)
    )

    result = await fetch_page("https://example.com")
    
    assert result["title"] == ""
    assert result["content"] == ""
    assert "Client error '404 Not Found'" in result["error"] or "404" in result["error"]
