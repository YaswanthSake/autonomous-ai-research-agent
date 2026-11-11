
import pytest

from app.agents.citation_utils import (
    validate_citations,
    generate_source_references,
)


@pytest.fixture
def source_registry():
    return {
        "S1": {
            "title": "Healthcare AI Research",
            "url": "https://example.com/healthcare",
        },
        "S2": {
            "title": "AI Medical Report",
            "url": "https://example.com/medical",
        },
    }


def test_valid_citations(source_registry):
    report = "AI is transforming healthcare [S1]."

    cited_ids = validate_citations(report, source_registry)

    assert cited_ids == {"S1"}


def test_invalid_citation_raises_error(source_registry):
    report = "AI is transforming healthcare [S3]."

    with pytest.raises(ValueError):
        validate_citations(report, source_registry)


def test_multiple_valid_citations(source_registry):
    report = "AI improves healthcare [S1] and diagnostics [S2]."

    cited_ids = validate_citations(report, source_registry)

    assert cited_ids == {"S1", "S2"}


def test_generate_source_references(source_registry):
    references = generate_source_references(
        {"S1", "S2"},
        source_registry,
    )

    assert "[S1] Healthcare AI Research" in references
    assert "https://example.com/healthcare" in references
    assert "[S2] AI Medical Report" in references


def test_no_citations_returns_empty_string(source_registry):
    references = generate_source_references(
        set(),
        source_registry,
    )

    assert references == ""
