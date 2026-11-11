# os- it allows python to access environment variables
import os
# load_dotenv()- loads variables from .env file.

from dotenv import load_dotenv

load_dotenv()

# Choose whether to use a mock model or the real Gemini API
USE_MOCK_LLM = os.getenv("USE_MOCK_LLM", "false").lower() == "true"
"""
USE_MOCK_LLM reads a setting from your .env file.
When it's true, the application won't require a Gemini API key.
When it's false, the application will use Gemini and require your API key.
"""
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# An API key is required only when using the real Gemini model
if not USE_MOCK_LLM and not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")

# Tavily provide search results to the agents
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is missing. Check your .env file.")