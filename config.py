import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Gemini API Key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# SerpAPI Key (Google Search)
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# Basic validation (optional but good practice)
if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY not found in .env file")

if not SERPAPI_KEY:
    raise ValueError("❌ SERPAPI_KEY not found in .env file")
