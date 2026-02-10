import os
from pathlib import Path

# 1. Define BASE_DIR to prevent the NameError in other files
BASE_DIR = Path(__file__).resolve().parent

# 2. Get keys directly from the environment (Render Environment Group)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")

# 3. Validation that won't crash the build process unnecessarily
if not GEMINI_API_KEY:
    print("⚠️ WARNING: GEMINI_API_KEY is not set.")

if not SERPAPI_KEY:
    print("⚠️ WARNING: SERPAPI_KEY is not set.")