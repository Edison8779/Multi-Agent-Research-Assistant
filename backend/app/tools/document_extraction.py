import io
from typing import Any

from bs4 import BeautifulSoup
from pypdf import PdfReader


def extract_text_from_html(html_content: str) -> str:
    """Extract clean text from HTML content."""
    soup = BeautifulSoup(html_content, "html.parser")
    # Remove script and style elements
    for element in soup(["script", "style", "nav", "footer", "header", "noscript"]):
        element.decompose()
    
    text = soup.get_text(separator=" ")
    return " ".join(text.split())


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from a PDF file using pypdf."""
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text_parts = []
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text_parts.append(extracted)
    
    return " ".join(text_parts)


def extract_document(content: bytes, mime_type: str) -> dict[str, Any]:
    """
    Extract clean text from a document based on its MIME type.
    Supports text/plain, text/html, text/markdown, and application/pdf.
    """
    try:
        if mime_type == "application/pdf":
            text = extract_text_from_pdf(content)
        elif mime_type in ["text/html", "application/xhtml+xml"]:
            text = extract_text_from_html(content.decode("utf-8", errors="replace"))
        elif mime_type in ["text/plain", "text/markdown", "text/csv"]:
            text = content.decode("utf-8", errors="replace")
        else:
            return {"text": "", "error": f"Unsupported MIME type: {mime_type}"}
            
        return {"text": text.strip(), "error": None}
    
    except Exception as e:
        return {"text": "", "error": str(e)}
