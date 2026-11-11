
import re

from langchain_core.messages import HumanMessage, SystemMessage

from app.agents.state import ResearchState
from app.agents.llm import llm
from app.agents.model_utils import invoke_llm_with_retry
from app.agents.citation_utils import (
    validate_citations,
    generate_source_references,
)


def synthesizer_node(state: ResearchState) -> dict:
    """
    Analyze collected research and generate a report
    with validated references.
    """

    print("\nStarting final research synthesis...")

    research_material = []
    source_registry = {}
    source_number = 1

    # Step 1: Assign unique IDs to collected sources
    for finding in state["research_findings"]:

        research_material.append(
            f"\nResearch task: {finding['task']}\n"
        )

        for source in finding["sources"]:

            source_id = f"S{source_number}"
            source_registry[source_id] = source

            research_material.append(
                f"""
Source ID: [{source_id}]
Title: {source.get('title', '')}
URL: {source.get('url', '')}
Content: {source.get('content', '')[:2000]}
"""
            )

            source_number += 1

    combined_research = "\n".join(research_material)

    # Step 2: Prepare Gemini messages
    messages = [
        SystemMessage(
            content=(
                "You are an expert research analyst. "
                "Create a detailed and structured research report. "
                "Use only the supplied research evidence. "
                "Cite factual claims using the provided source IDs, "
                "for example [S1] or [S2]. "
                "Never invent source IDs, URLs, statistics, or facts. "
                "If evidence is insufficient, explicitly state so. "
                "Do not create a separate bibliography; the application "
                "will generate the source list."
            )
        ),
        HumanMessage(
            content=(
                f"Research topic: {state['topic']}\n\n"
                f"Research plan:\n"
                f"{chr(10).join(state['research_plan'])}\n\n"
                f"Collected research evidence:\n"
                f"{combined_research}\n\n"
                "Produce a consolidated research report with clear headings."
            )
        ),
    ]

    # Step 3: Generate the report with one Gemini call
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

    # Step 4: Validate citation IDs
    cited_ids = validate_citations(
        final_report,
        source_registry,
    )

    # Step 5: Generate verified source references
    final_report += generate_source_references(
        cited_ids,
        source_registry,
    )

    print("Final research synthesis completed.")
    print(f"Validated citations: {len(cited_ids)}")

    return {
        "final_report": final_report,
        "status": "completed",
    }
