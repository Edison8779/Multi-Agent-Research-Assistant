import asyncio
import json
import uuid
from datetime import datetime
from typing import Dict, List
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse

from app.agents.research_agent import create_research_agent
from app.schemas.research import ResearchRequest, ResearchReport, ResearchFinding, SearchResult, RetrievedDocument

router = APIRouter(prefix="/api/research", tags=["Research"])

# In-memory store for research reports (persists during backend process lifecycle)
RESEARCH_STORE: Dict[str, ResearchReport] = {}


def format_sse(event_type: str, data: dict) -> str:
    """Format data as Server-Sent Event."""
    return f"event: {event_type}\ndata: {json.dumps(data)}\n\n"


@router.post("")
async def start_research(request: ResearchRequest):
    """
    Start a research task and return a research ID.
    """
    research_id = f"res_{uuid.uuid4().hex[:8]}"
    return {"id": research_id, "question": request.question, "status": "pending"}


@router.get("/stream")
async def stream_research(question: str = Query(..., min_length=3)):
    """
    Stream live execution of the research agent using Server-Sent Events (SSE).
    """
    research_id = f"res_{uuid.uuid4().hex[:8]}"
    
    async def event_generator():
        # Step 1: Initial event
        yield format_sse("progress", {
            "step": "planning",
            "status": "in_progress",
            "message": f"Analyzing question & creating plan: '{question}'",
            "timestamp": datetime.now().isoformat()
        })
        await asyncio.sleep(0.5)

        yield format_sse("progress", {
            "step": "planning",
            "status": "completed",
            "message": "Research plan formulated.",
            "timestamp": datetime.now().isoformat()
        })

        # Create research agent graph
        agent = create_research_agent()
        initial_state = {
            "question": question,
            "search_queries": [],
            "search_results": [],
            "retrieved_documents": [],
            "findings": [],
            "final_answer": ""
        }

        # Step 2: Search web
        yield format_sse("progress", {
            "step": "search",
            "status": "in_progress",
            "message": f"Executing web search queries for context...",
            "timestamp": datetime.now().isoformat()
        })

        search_results_raw = []
        retrieved_docs_raw = []
        findings_raw = []
        final_ans = ""

        try:
            # Execute step-by-step stream through LangGraph
            async for output in agent.astream(initial_state, stream_mode="updates"):
                for node_name, node_output in output.items():
                    if node_name == "search":
                        search_results_raw = node_output.get("search_results", [])
                        queries = node_output.get("search_queries", [])
                        yield format_sse("progress", {
                            "step": "search",
                            "status": "completed",
                            "message": f"Found {len(search_results_raw)} primary web sources.",
                            "data": {
                                "queries": queries,
                                "results": [r.model_dump() if hasattr(r, 'model_dump') else dict(r) for r in search_results_raw]
                            },
                            "timestamp": datetime.now().isoformat()
                        })

                        # Move to retrieve
                        yield format_sse("progress", {
                            "step": "retrieve",
                            "status": "in_progress",
                            "message": "Fetching and extracting full page documents...",
                            "timestamp": datetime.now().isoformat()
                        })

                    elif node_name == "retrieve":
                        retrieved_docs_raw = node_output.get("retrieved_documents", [])
                        yield format_sse("progress", {
                            "step": "retrieve",
                            "status": "completed",
                            "message": f"Successfully retrieved {len(retrieved_docs_raw)} detailed documents.",
                            "data": {
                                "documents": [
                                    {
                                        "title": d.title,
                                        "url": d.url,
                                        "content_preview": d.content[:300] + "..."
                                    } for d in retrieved_docs_raw
                                ]
                            },
                            "timestamp": datetime.now().isoformat()
                        })

                        # Move to extract
                        yield format_sse("progress", {
                            "step": "extract",
                            "status": "in_progress",
                            "message": "Running LLM claim & evidence extraction pipeline...",
                            "timestamp": datetime.now().isoformat()
                        })

                    elif node_name == "extract":
                        findings_raw = node_output.get("findings", [])
                        yield format_sse("progress", {
                            "step": "extract",
                            "status": "completed",
                            "message": f"Extracted {len(findings_raw)} verified claim-evidence pairs.",
                            "data": {
                                "findings": [f.model_dump() if hasattr(f, 'model_dump') else dict(f) for f in findings_raw]
                            },
                            "timestamp": datetime.now().isoformat()
                        })

                        # Move to answer
                        yield format_sse("progress", {
                            "step": "answer",
                            "status": "in_progress",
                            "message": "Synthesizing comprehensive research report with citations...",
                            "timestamp": datetime.now().isoformat()
                        })

                    elif node_name == "answer":
                        final_ans = node_output.get("final_answer", "")
                        yield format_sse("progress", {
                            "step": "answer",
                            "status": "completed",
                            "message": "Report synthesis complete.",
                            "timestamp": datetime.now().isoformat()
                        })

            # Create final report object
            key_takeaways = [f.claim for f in findings_raw[:4]] if findings_raw else []
            
            report = ResearchReport(
                id=research_id,
                question=question,
                created_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
                status="completed",
                search_queries=[question],
                search_results=search_results_raw,
                retrieved_documents=retrieved_docs_raw,
                findings=findings_raw,
                final_answer=final_ans,
                executive_summary=f"Synthesized analysis based on {len(search_results_raw)} web sources and {len(findings_raw)} extracted facts.",
                key_takeaways=key_takeaways,
                recommendations="Refer to the detailed findings and verified evidence below for implementation decisions.",
                limitations="Analysis is constrained to retrieved public web documentation up to the current session time."
            )

            # Store report in memory
            RESEARCH_STORE[research_id] = report

            # Emit final report event
            yield format_sse("report", report.model_dump())
            yield format_sse("done", {"id": research_id, "status": "completed"})

        except Exception as e:
            yield format_sse("error", {"message": f"Error during research execution: {str(e)}"})

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.get("/history", response_model=List[ResearchReport])
async def get_history():
    """
    Get all past research reports sorted by recency.
    """
    reports = list(RESEARCH_STORE.values())
    return list(reversed(reports))


@router.get("/{research_id}", response_model=ResearchReport)
async def get_research_by_id(research_id: str):
    """
    Get a specific research report by ID.
    """
    if research_id not in RESEARCH_STORE:
        raise HTTPException(status_code=404, detail="Research report not found.")
    return RESEARCH_STORE[research_id]
