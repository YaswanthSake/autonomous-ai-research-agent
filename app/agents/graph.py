
from langgraph.graph import StateGraph, START, END

from app.agents.state import ResearchState
from app.agents.planner import planner_node
from app.agents.researcher import researcher_node
from app.agents.synthesizer import synthesizer_node


def build_research_graph():
    """
    Build the autonomous research workflow.

    Planner -> Researcher -> Synthesizer
    """

    workflow = StateGraph(ResearchState)

    # Register workflow nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # Define execution order
    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "synthesizer")
    workflow.add_edge("synthesizer", END)

    return workflow.compile()


research_graph = build_research_graph()
