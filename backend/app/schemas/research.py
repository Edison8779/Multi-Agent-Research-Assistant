from typing import Any, List, Optional
from typing_extensions import TypedDict
from pydantic import BaseModel, Field

class ResearchFinding(BaseModel):
    """
    A single factual finding extracted from a source during research.
    """
    claim: str = Field(description="The factual claim extracted from the text.")
    evidence: str = Field(description="The specific text snippet or data point supporting the claim.")
    source_url: str = Field(description="The URL of the source document.")
    source_title: str = Field(description="The title of the source document.")
    confidence: float = Field(description="Confidence score from 0.0 to 1.0 that this claim is accurate and supported.", ge=0.0, le=1.0)


class SearchResult(BaseModel):
    """
    A single web search result.
    """
    title: str
    url: str
    snippet: str


class RetrievedDocument(BaseModel):
    """
    Content retrieved from a URL.
    """
    title: str
    url: str
    content: str
    published_date: Optional[str] = None


class FindingsExtraction(BaseModel):
    """
    Wrapper for extracting a list of findings.
    """
    findings: List[ResearchFinding]


class ResearchState(TypedDict):
    """
    State representing the context of a single research agent execution.
    """
    question: str
    search_queries: List[str]
    search_results: List[SearchResult]
    retrieved_documents: List[RetrievedDocument]
    findings: List[ResearchFinding]
    final_answer: str


class ResearchRequest(BaseModel):
    question: str = Field(..., min_length=3, description="The research question to analyze.")


class ResearchReport(BaseModel):
    id: str
    question: str
    created_at: str
    status: str = "completed"
    search_queries: List[str] = []
    search_results: List[SearchResult] = []
    retrieved_documents: List[RetrievedDocument] = []
    findings: List[ResearchFinding] = []
    final_answer: str
    executive_summary: Optional[str] = None
    key_takeaways: List[str] = []
    recommendations: Optional[str] = None
    limitations: Optional[str] = None

