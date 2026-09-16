import os
import asyncio
from groq import AsyncGroq

async def main():
    client = AsyncGroq(api_key=os.environ.get('LLM_API_KEY') )
    
    models_to_test = [
        "llama-3.1-8b-instant"
        
    ]
    
    for model in models_to_test:
        try:
            print(f"Testing {model}...")
            await client.chat.completions.create(
                model=model,
                messages=[{'role': 'user', 'content': 'hi'}]
            )
            print(f"OK: {model} WORKS!")
            break
        except Exception as e:
            print(f"FAIL: {model} failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
