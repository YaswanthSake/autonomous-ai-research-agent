"""
TypeDict--- it gives us a structured way to define the expected
state fields and their types.
"""
from typing import TypedDict

"""
The state is the shared data structure that flow through 
our LangGraph workflow.

Also the response store here, like research plan, research findings.
"""
class ResearchSource(TypedDict, total=False):
    title: str
    url: str
    content: str
    score: float

class ResearchFinding(TypedDict, total=False):
    task: str
    summary: str
    sources: list[ResearchSource]

class ResearchState(TypedDict):
    topic: str
    research_plan: list[str]
    research_findings: list[ResearchFinding]
    final_report: str
    status: str