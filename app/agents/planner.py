from app.agents.state import ResearchState

# In LangGraph, a node is a function that perform a particlualar taks.
"""
Planner_node-->
1. Receives the current state.
2. Reads the research topic.
3. Generate a research plan.
4. Return state updates.
"""
def planner_node(state: ResearchState) -> dict:
    """
    Generate a basic research plan from the given topic.
    """

    topic = state["topic"]

    plan = [
        f"Understand the fundamentals of {topic}",
        f"Identify important concepts related to {topic}",
        f"Explore real-world appliction of {topic}",
        f"Analyze challenges and limitations of {topic}",
        f"Prepare a comprehensive report of {topic}"
    ]

    return {
        "research_plan": plan,
        "status": "planned",
    }
