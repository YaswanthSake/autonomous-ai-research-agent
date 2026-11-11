
from app.agents.state import ResearchState, ResearchFinding
from app.agents.search import search_web


def researcher_node(state: ResearchState) -> dict:
    """
    Execute web searches for every research task and collect structured sources.
    Gemini is intentionally not called in this node.
    """

    findings: list[ResearchFinding] = []

    for task in state["research_plan"]:

        print(f"\nStarting research task: {task}")

        # Step 1: Search the web using Tavily
        search_results = search_web(task)

        print(f"Search completed for: {task}")

        # Step 2: Extract source information
        sources = []

        for result in search_results.get("results", []):
            sources.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),
                "score": result.get("score", 0.0),
            })

        # Step 3: Store search results without Gemini analysis
        findings.append({
            "task": task,
            "summary": "Search results collected. Pending final analysis.",
            "sources": sources,
        })

    print("\nAll research searches completed.")

    return {
        "research_findings": findings,
        "status": "researched",
    }
