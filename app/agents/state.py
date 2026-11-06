"""
TypeDict--- it gives us a structured way to define the expected
state fields and their types.
"""
from typing import TypedDict

"""
The state is the shared data structure that flow through 
our LangGraph workflow.
"""
class ResearchState(TypedDict):
    topic: str
    research_plan: list[str]
    status: str

