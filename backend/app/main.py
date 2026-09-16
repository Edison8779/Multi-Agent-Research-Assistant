from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.research import router as research_router

app = FastAPI(
    title="Multi-Agent Research Assistant API",
    description="Backend API for the Multi-Agent Research Assistant",
    version="0.1.0",
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exactly the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    """
    Health check endpoint.
    """
    return {"status": "ok", "message": "Backend is running"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
