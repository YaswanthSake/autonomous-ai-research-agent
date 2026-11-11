"""
-The user sends a POST request.
-FastAPI validates the request using ResearchRequest.
-We construct the initial LangGraph state.
-ainvoke() executes the graph asynchronously.
-`We convert the result into a validated response.
"""
from fastapi import APIRouter

from app.agents.graph import research_graph
from app.schemas.request import ResearchRequest, ResearchResponse


router = APIRouter()


@router.post(
    "/research",
    response_model=ResearchResponse,
    tags=["Research Agent"],
)
async def create_research_plan(request: ResearchRequest):
    """
    Generate a research plan using the LangGraph workflow.
    """

    initial_state = {
        "topic": request.topic,
        "research_plan": [],
        "research_findings": [],
        "final_report": "",
        "status": "pending",
    }

    result = await research_graph.ainvoke(initial_state)

    return ResearchResponse(
        topic=result["topic"],
        research_plan=result["research_plan"],
        research_findings=result["research_findings"],
        final_report=result["final_report"],
        status=result["status"],
    )
