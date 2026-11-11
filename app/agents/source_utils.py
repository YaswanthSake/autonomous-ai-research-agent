
def filter_and_deduplicate_sources(
    results: list[dict],
    seen_urls: set[str],
    min_score: float = 0.3,
) -> list[dict]:
    """
    Remove incomplete, low-relevance, and duplicate search results.
    """

    sources = []

    for result in results:
        title = result.get("title", "").strip()
        url = result.get("url", "").strip()
        content = result.get("content", "").strip()
        score = float(result.get("score") or 0.0)

        if not title or not url or not content:
            continue

        if score < min_score:
            continue

        normalized_url = url.rstrip("/").lower()

        if normalized_url in seen_urls:
            continue

        seen_urls.add(normalized_url)

        sources.append({
            "title": title,
            "url": url,
            "content": content,
            "score": score,
        })

    return sources
