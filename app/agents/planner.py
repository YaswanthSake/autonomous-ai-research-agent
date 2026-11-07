from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential

from app.core.config import GOOGLE_API_KEY, GEMINI_MODEL
from app.agents.state import ResearchState


llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
)

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=2, max=10),
    reraise=True,
)
def generate_research_plan(messages):
    return llm.invoke(messages)

def planner_node(state: ResearchState) -> dict:
    """
    Generate a research plan using Google's Gemini LLM.
    """

    topic = state["topic"]

    messages = [
        SystemMessage(
            content=(
                "You are an expert AI research planner. "
                "Create exactly 5 detailed, logical research tasks "
                "for the given topic. Return one task per line, "
                "numbered from 1 to 5. Do not add an introduction."
            )
        ),
        HumanMessage(
            content=f"Create a research plan for: {topic}"
        ),
    ]

    # response = llm.invoke(messages)
    response = generate_research_plan(messages)

    content = response.content

    if isinstance(content, list):
        text_content = "\n".join(
            block["text"]
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    else:
        text_content = str(content)

    plan = [
        line.strip().lstrip("0123456789.-) ").strip()
        for line in text_content.splitlines()
        if line.strip()
    ]

    return {
        "research_plan": plan,
        "status": "planned",
    }