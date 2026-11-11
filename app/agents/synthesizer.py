
from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.state import ResearchState
from app.agents.llm import llm
from app.agents.model_utils import invoke_llm_with_retry


def synthesizer_node(state: ResearchState) -> dict:
    """
    Analyze all collected web search results in one Gemini call
    and generate a consolidated research report.
    """

    print("\nStarting final research synthesis...")

    # Step 1: Prepare all collected research evidence
    research_material = []

    for finding in state["research_findings"]:
        research_material.append(
            f"\nResearch task: {finding['task']}\n"
            f"Sources:\n"
        )

        for source in finding["sources"]:
            research_material.append(
                f"""
Title: {source.get('title', '')}
URL: {source.get('url', '')}
Content: {source.get('content', '')[:2000]}
Relevance score: {source.get('score', 0.0)}
"""
            )

    combined_research = "\n".join(research_material)

    # Step 2: Prepare Gemini messages
    messages = [
        SystemMessage(
            content=(
                "You are an expert research analyst. "
                "Produce a detailed, well-structured research report "
                "using the supplied web search evidence. "
                "Organize the report with clear headings. "
                "Compare findings across sources where useful. "
                "Distinguish established facts from uncertainty. "
                "Include source URLs alongside relevant claims. "
                "Never invent facts, statistics, or sources. "
                "If evidence is insufficient, explicitly say so."
            )
        ),
        HumanMessage(
            content=(
                f"Research topic: {state['topic']}\n\n"
                f"Research plan:\n"
                f"{chr(10).join(state['research_plan'])}\n\n"
                f"Collected web research:\n"
                f"{combined_research}\n\n"
                "Create one consolidated research report."
            )
        ),
    ]

    # Step 3: Make one Gemini call for the complete analysis
    response = invoke_llm_with_retry(llm, messages)

    content = response.content

    if isinstance(content, list):
        final_report = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict)
            and block.get("type") == "text"
        )
    else:
        final_report = str(content)

    print("Final research synthesis completed.")

    # Step 4: Return the completed report
    return {
        "final_report": final_report,
        "status": "completed",
    }
