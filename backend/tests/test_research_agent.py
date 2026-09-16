import pytest
from app.agents.research_agent import create_research_agent
from app.schemas.research import ResearchState

@pytest.mark.asyncio
async def test_research_agent_compiles():
    """
    Test that the LangGraph compiles without errors.
    """
    agent = create_research_agent()
    assert agent is not None

@pytest.mark.asyncio
async def test_research_agent_execution(monkeypatch):
    """
    Test a basic execution with mocked tools.
    """
    # Mock search
    async def mock_search_web(query, max_results=5):
        return [{"title": "PostgreSQL", "url": "https://postgresql.org", "snippet": "Advanced DB"}]
        
    monkeypatch.setattr("app.agents.research_agent.search_web", mock_search_web)
    
    # Mock retrieve
    async def mock_fetch_page(url):
        return {"title": "PostgreSQL", "url": url, "content": "PostgreSQL is great.", "error": None}
        
    monkeypatch.setattr("app.agents.research_agent.fetch_page", mock_fetch_page)
    
    # Mock LLM generation
    from app.schemas.research import FindingsExtraction, ResearchFinding
    from app.core.llm import TokenUsage
    
    async def mock_generate_structured(*args, **kwargs):
        finding = ResearchFinding(
            claim="PostgreSQL is great.",
            evidence="PostgreSQL is great.",
            source_url="https://postgresql.org",
            source_title="PostgreSQL",
            confidence=0.9
        )
        return FindingsExtraction(findings=[finding]), TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20, estimated_cost_usd=0.0)
        
    monkeypatch.setattr("app.agents.research_agent.generate_structured", mock_generate_structured)
    
    from app.core.llm import LLMResponse
    async def mock_generate_text(*args, **kwargs):
        return LLMResponse(
            content="Based on findings, PostgreSQL is great.",
            usage=TokenUsage(prompt_tokens=10, completion_tokens=10, total_tokens=20, estimated_cost_usd=0.0)
        )
        
    monkeypatch.setattr("app.agents.research_agent.generate_text", mock_generate_text)
    
    agent = create_research_agent()
    
    initial_state = {"question": "What is PostgreSQL?"}
    
    final_state = await agent.ainvoke(initial_state)
    
    assert final_state["question"] == "What is PostgreSQL?"
    assert len(final_state["search_results"]) == 1
    assert len(final_state["retrieved_documents"]) == 1
    assert len(final_state["findings"]) == 1
    assert final_state["final_answer"] == "Based on findings, PostgreSQL is great."
