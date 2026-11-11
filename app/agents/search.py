from langchain_tavily import TavilySearch

from app.core.config import TAVILY_API_KEY


# Initialize Tavily search tool
search_tool = TavilySearch(
    max_results=5,
    topic="general",
)


def search_web(query: str) -> dict:
    """
    Search the web using Tavily.

    Args:
        query: Research query to search for.

    Returns:
        Search results returned by Tavily.
    """

    results = search_tool.invoke({
        "query": query
    })

    return results