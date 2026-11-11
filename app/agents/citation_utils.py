
import re


def validate_citations(
    report: str,
    source_registry: dict,
) -> set[str]:
    """
    Validate that every citation ID in the report
    exists in the source registry.
    """

    cited_ids = set(
        re.findall(r"\[(S\d+)\]", report)
    )

    invalid_ids = cited_ids - set(source_registry.keys())

    if invalid_ids:
        raise ValueError(
            f"Report contains unknown source IDs: {sorted(invalid_ids)}"
        )

    return cited_ids


def generate_source_references(
    cited_ids: set[str],
    source_registry: dict,
) -> str:
    """
    Generate references using only verified source metadata.
    """

    if not cited_ids:
        return ""

    references = ["\n\n## Sources\n"]

    for source_id in sorted(
        cited_ids,
        key=lambda item: int(item[1:])
    ):
        source = source_registry[source_id]

        references.append(
            f"- [{source_id}] "
            f"{source.get('title', 'Untitled source')} "
            f"— {source.get('url', '')}"
        )

    return "\n".join(references)
