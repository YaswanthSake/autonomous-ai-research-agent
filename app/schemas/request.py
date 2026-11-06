"""
Why Pyadantic -->
Ex- Empty topic are rejected
Topics shorter than 3 char are rejected
Topics longer than 500 char are rejected
API responsed follow a defined structure
"""
from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=3,
        max_length=500,
        description="The research topic provided by the user",
    )

class ResearchResponse(BaseModel):
    topic: str
    research_plan: list[str]
    status: str
