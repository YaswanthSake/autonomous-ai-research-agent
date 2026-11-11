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

# Describes one webpage
class ResearchSource(BaseModel):
    title: str
    url: str
    content: str
    score: float

# Describes one research task's result
class ResearchFinding(BaseModel):
    task: str
    summary: str
    sources: list[ResearchSource]

# Describes the complete API response
class ResearchResponse(BaseModel):
    topic: str
    research_plan: list[str]
    research_findings: list[ResearchFinding]
    final_report: str
    status: str
