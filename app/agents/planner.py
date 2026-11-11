from langchain_core.messages import SystemMessage, HumanMessage
from app.agents.llm import llm

from app.agents.model_utils import invoke_llm_with_retry
from app.agents.state import ResearchState


# llm = ChatGoogleGenerativeAI(
#     model=GEMINI_MODEL,
#     google_api_key=GOOGLE_API_KEY,
#     temperature=0,
# )

def should_retry(exception):
    """
    Retry only temporary errors.
    Do not retry quota or billing errors.
    """

    error_message = str(exception).lower()

    # Stop immediately for quota and billing errors
    if "429" in error_message or "resource_exhausted" in error_message:
        return False

    if "402" in error_message or "payment required" in error_message:
        return False

    # Retry temporary server and network errors
    if any(code in error_message for code in ["503", "504", "500"]):
        return True

    if any(
        keyword in error_message
        for keyword in ["timeout", "timed out", "connection error"]
    ):
        return True

    # Do not retry unknown errors
    return False



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
    response = invoke_llm_with_retry(llm, messages)

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
    # print("Plan:", plan)
    return {
        "research_plan": plan,
        "status": "planned",
    }