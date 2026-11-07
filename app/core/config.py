# os- it allows python to access environment variables
import os
# load_dotenv()- loads variables from .env file.

from dotenv import load_dotenv

load_dotenv()

# os.getenv()- retrieves a configuration value.
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GEMINI_MODEL- select which Gemini model to use.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Check your .env file.")