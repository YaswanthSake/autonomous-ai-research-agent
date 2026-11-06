# Build the LangGraph workflow
from langgraph.graph import StateGraph, START, END

from app.agents.state import ResearchState
from app.agents.planner import planner_node

def build_research_graph():
    """
    Build and compile the research agent workflow.
    """
    workflow = StateGraph(ResearchState)

    # Register the planner node
    workflow.add_node("planner", planner_node)

    # Define workflow execution order
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", END)

    # Compile the graph

    return workflow.compile()

research_graph = build_research_graph()