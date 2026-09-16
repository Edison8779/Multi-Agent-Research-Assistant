import json
from typing import Dict, Any

from langgraph.graph import StateGraph, START, END

from app.core.llm import generate_structured, generate_text
from app.schemas.research import ResearchState, SearchResult, RetrievedDocument, FindingsExtraction
from app.tools.web_search import search_web
from app.tools.web_retrieval import fetch_page


async def search_node(state: ResearchState) -> Dict[str, Any]:
    """
    Search the web for the given question.
    """
    question = state["question"]
    # For now, just use the question as the query directly
    # In a more advanced version, we'd use an LLM to generate queries
    results = await search_web(question, max_results=3)
    
    search_results = [
        SearchResult(title=r["title"], url=r["url"], snippet=r["snippet"])
        for r in results
    ]
    return {"search_results": search_results, "search_queries": [question]}


async def retrieve_node(state: ResearchState) -> Dict[str, Any]:
    """
    Retrieve content for the top search results.
    """
    results = state.get("search_results", [])
    retrieved_documents = []
    
    # We'll just fetch the top 2 to keep it fast
    urls_to_fetch = [r.url for r in results[:2]]
    
    for url in urls_to_fetch:
        page_data = await fetch_page(url)
        if not page_data.get("error"):
            retrieved_documents.append(
                RetrievedDocument(
                    title=page_data["title"],
                    url=page_data["url"],
                    content=page_data["content"][:5000],  # truncate to avoid huge context
                )
            )
            
    return {"retrieved_documents": retrieved_documents}


async def extract_node(state: ResearchState) -> Dict[str, Any]:
    """
    Extract factual findings from the retrieved documents.
    """
    question = state["question"]
    documents = state.get("retrieved_documents", [])
    
    if not documents:
        return {"findings": []}
        
    context = ""
    for doc in documents:
        context += f"\n\nSource: {doc.title} ({doc.url})\n"
        context += doc.content
        
    prompt = f"""
    Research Question: {question}
    
    Based on the following source documents, extract factual claims that help answer the question.
    Only extract information that is explicitly stated in the sources.
    
    Sources:
    {context}
    """
    
    system_message = "You are a precise research assistant. Extract factual findings and output them as structured data."
    
    # Call the LLM to get structured output matching FindingsExtraction schema
    extracted_data, _ = await generate_structured(
        prompt=prompt,
        response_model=FindingsExtraction,
        system_message=system_message,
        temperature=0.0
    )
    
    return {"findings": extracted_data.findings}


async def answer_node(state: ResearchState) -> Dict[str, Any]:
    """
    Synthesize the findings into a final answer.
    """
    question = state["question"]
    findings = state.get("findings", [])
    
    if not findings:
        return {"final_answer": "I could not find enough reliable information to answer this question."}
        
    findings_text = ""
    for i, finding in enumerate(findings, 1):
        findings_text += f"\n{i}. {finding.claim}\n"
        findings_text += f"   Evidence: {finding.evidence}\n"
        findings_text += f"   Source: {finding.source_title} ({finding.source_url})\n"
        
    prompt = f"""
    Research Question: {question}
    
    Based on the following extracted findings, write a clear, concise, and accurate answer to the question.
    Cite your sources by mentioning the source title or URL.
    
    Findings:
    {findings_text}
    """
    
    system_message = "You are an expert synthesizer. Write a comprehensive answer based ONLY on the provided findings."
    
    response = await generate_text(
        prompt=prompt,
        system_message=system_message,
        temperature=0.3
    )
    
    return {"final_answer": response.content}


def create_research_agent():
    """
    Create and compile the LangGraph for the Single Research Agent.
    """
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("search", search_node)
    workflow.add_node("retrieve", retrieve_node)
    workflow.add_node("extract", extract_node)
    workflow.add_node("answer", answer_node)
    
    # Linear flow
    workflow.add_edge(START, "search")
    workflow.add_edge("search", "retrieve")
    workflow.add_edge("retrieve", "extract")
    workflow.add_edge("extract", "answer")
    workflow.add_edge("answer", END)
    
    app = workflow.compile()
    return app
