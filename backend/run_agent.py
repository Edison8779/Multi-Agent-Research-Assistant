import asyncio
import sys
from app.agents.research_agent import create_research_agent
from pprint import pprint

# Fix Windows console encoding for Unicode characters from LLM responses
sys.stdout.reconfigure(encoding="utf-8")

async def main():
    agent = create_research_agent()
    question = "What are the advantages of PostgreSQL?"
    
    print(f"Researching: {question}\n")
    
    # Use ainvoke for asynchronous execution of the graph
    result = await agent.ainvoke({"question": question})
    
    print("--- FINDINGS ---")
    for i, finding in enumerate(result.get("findings", [])):
        print(f"\nFinding {i+1}: {finding.claim}")
        print(f"Confidence: {finding.confidence}")
        print(f"Source: {finding.source_url}")
        
    print("\n--- FINAL ANSWER ---")
    print(result.get("final_answer", ""))

if __name__ == "__main__":
    asyncio.run(main())
