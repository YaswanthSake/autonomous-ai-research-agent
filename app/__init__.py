
from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Autonomous AI Research Agent",
    description="An AI-powered research agent built with FastAPI and LangGraph.",
    version="0.1.0",
)

# Register API routes
app.include_router(router)


@app.get("/", tags=["General"])
async def root():
    return {
        "message": "Autonomous AI Research Agent API is running",
        "status": "healthy",
    }


@app.get("/health", tags=["General"])
async def health_check():
    return {
        "status": "healthy",
        "service": "research-agent",
    }
