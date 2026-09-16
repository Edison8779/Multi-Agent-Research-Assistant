import io
from pypdf import PdfWriter, PdfReader

from app.tools.document_extraction import (
    extract_text_from_html,
    extract_text_from_pdf,
    extract_document,
)


def test_extract_text_from_html():
    html = "<html><body><script>bad</script><p>good text</p></body></html>"
    text = extract_text_from_html(html)
    assert text == "good text"


def test_extract_document_plain_text():
    content = b"Hello world"
    result = extract_document(content, "text/plain")
    assert result["text"] == "Hello world"
    assert result["error"] is None


def test_extract_document_html():
    content = b"<html><body><p>Hello world</p></body></html>"
    result = extract_document(content, "text/html")
    assert result["text"] == "Hello world"
    assert result["error"] is None


def test_extract_document_unsupported():
    content = b"fake image data"
    result = extract_document(content, "image/png")
    assert result["text"] == ""
    assert "Unsupported MIME type" in result["error"]


def test_extract_document_pdf():
    # pypdf requires a valid PDF. 
    # For a simple test, we will just use a try-except or mock, 
    # but let's test the error handling of a bad PDF first.
    content = b"Not a real PDF"
    result = extract_document(content, "application/pdf")
    assert result["text"] == ""
    assert result["error"] is not None
