
from app.agents.source_utils import filter_and_deduplicate_sources


def test_filters_low_score_sources():
    results = [
        {
            "title": "Good source",
            "url": "https://example.com/good",
            "content": "Useful research content",
            "score": 0.9,
        },
        {
            "title": "Weak source",
            "url": "https://example.com/weak",
            "content": "Weak research content",
            "score": 0.1,
        },
    ]

    sources = filter_and_deduplicate_sources(results, set())

    assert len(sources) == 1
    assert sources[0]["title"] == "Good source"


def test_removes_duplicate_urls():
    results = [
        {
            "title": "Source one",
            "url": "https://example.com/article/",
            "content": "First result",
            "score": 0.9,
        },
        {
            "title": "Source duplicate",
            "url": "https://example.com/article",
            "content": "Duplicate result",
            "score": 0.8,
        },
    ]

    sources = filter_and_deduplicate_sources(results, set())

    assert len(sources) == 1


def test_filters_incomplete_sources():
    results = [
        {
            "title": "",
            "url": "https://example.com/article",
            "content": "Some content",
            "score": 0.9,
        }
    ]

    sources = filter_and_deduplicate_sources(results, set())

    assert len(sources) == 0


def test_preserves_seen_urls_between_calls():
    seen_urls = set()

    first_results = [
        {
            "title": "First source",
            "url": "https://example.com/article",
            "content": "Research content",
            "score": 0.9,
        }
    ]

    second_results = [
        {
            "title": "Duplicate source",
            "url": "https://example.com/article",
            "content": "Research content again",
            "score": 0.8,
        }
    ]

    first = filter_and_deduplicate_sources(first_results, seen_urls)
    second = filter_and_deduplicate_sources(second_results, seen_urls)

    assert len(first) == 1
    assert len(second) == 0
