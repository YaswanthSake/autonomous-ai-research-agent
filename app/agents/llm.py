from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import (
    GOOGLE_API_KEY,
    GEMINI_MODEL,
    USE_MOCK_LLM,
)


class MockLLM:
    """
    A lightweight mock model for development without API calls.
    """

    def invoke(self, messages):
        prompt = "\n".join(
            str(message.content) for message in messages
        )

        if "research plan" in prompt.lower():
            topic = prompt.split("Research topic:")[-1].strip()

            response_text = f"""
1. Define the key concepts and background of {topic}.
2. Identify its major components and underlying principles.
3. Examine important applications and real-world use cases.
4. Analyze current challenges, limitations, and open questions.
5. Summarize key findings and possible future developments.
"""
        else:
            response_text = f"""
Mock research finding

This is simulated development output, not verified research.

The assigned task is:
{prompt.split("Research task:")[-1].strip()}

A real research step would gather evidence, evaluate reliable sources,
and summarize the findings. This mock response allows the application
workflow to be tested without making an API request.
"""

        return AIMessage(content=response_text)


if USE_MOCK_LLM:
    # if it true use mock llm
    llm = MockLLM()
else:
    # otherwise use real Gemini model
    llm = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0,
    )