
from app.agents.state import ResearchState, ResearchFinding
from app.agents.search import search_web
from app.agents.source_utils import filter_and_deduplicate_sources


def researcher_node(state: ResearchState) -> dict:
    """
    Search the web, filter weak results, and remove duplicate URLs.
    """

    findings: list[ResearchFinding] = []
    seen_urls: set[str] = set()

    for task in state["research_plan"]:

        print(f"\nStarting research task: {task}")

        search_results = search_web(task)

        print(f"Search completed for: {task}")

        sources = filter_and_deduplicate_sources(
            results=search_results.get("results", []),
            seen_urls=seen_urls,
            min_score=0.3,
        )

        findings.append({
            "task": task,
            "summary": "Search results collected and filtered.",
            "sources": sources,
        })

        print(f"Accepted {len(sources)} sources for: {task}")

    print("\nAll research searches completed.")

    return {
        "research_findings": findings,
        "status": "researched",
    }
