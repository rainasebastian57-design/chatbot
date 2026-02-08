import requests
import os

def serpapi_search(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": os.getenv("SERPAPI_KEY"),
        "engine": "google",
        "hl": "en",
        "gl": "in"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()
