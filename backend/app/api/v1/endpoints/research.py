from fastapi import APIRouter, HTTPException, status
from app.schemas.research import ResearchRequest, ResearchResponse
from app.agents.research_agent import create_research_agent

router = APIRouter()
_research_agent = None


def get_agent():
    global _research_agent
    if _research_agent is None:
        _research_agent = create_research_agent()
    return _research_agent


@router.post("/single", response_model=ResearchResponse, status_code=status.HTTP_200_OK)
async def run_single_research(request: ResearchRequest) -> ResearchResponse:
    """
    Execute single-agent research workflow for a given question.
    """
    try:
        agent = get_agent()
        result = await agent.ainvoke({"question": request.question})
        
        return ResearchResponse(
            question=request.question,
            search_queries=result.get("search_queries", []),
            search_results=result.get("search_results", []),
            retrieved_documents=result.get("retrieved_documents", []),
            findings=result.get("findings", []),
            final_answer=result.get("final_answer", "")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Research agent execution failed: {str(e)}"
        )
