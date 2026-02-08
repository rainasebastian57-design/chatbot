from google import genai
from conversation import Conversation
from search import serpapi_search
from config import GEMINI_API_KEY
import time

# Create Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Load conversation memory
conversation = Conversation()

# -------- Helper: detect real-time queries --------
def needs_realtime_data(user_input):
    keywords = [
        "weather", "temperature", "price", "bitcoin",
        "today", "current", "news", "now"
    ]
    return any(word in user_input.lower() for word in keywords)

print("🤖 Gemini Chatbot (type 'exit' to quit)\n")

# -------- Chat Loop --------
while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit"]:
        print("Goodbye 👋")
        break

    try:
        prompt = user_input

        # ---- REAL-TIME DATA FETCH ----
        if needs_realtime_data(user_input):
            search_data = serpapi_search(user_input)

            # Extract useful text
            realtime_info = ""

            if "answer_box" in search_data:
                realtime_info = str(search_data["answer_box"])
            elif "organic_results" in search_data:
                realtime_info = search_data["organic_results"][0].get("snippet", "")
            else:
                realtime_info = "No real-time data found."

            prompt = f"""
            Use the following REAL-TIME information from Google Search
            to answer accurately. Do not hallucinate.

            Real-time data:
            {realtime_info}

            User question:
            {user_input}
            """

        # ---- GEMINI RESPONSE ----
        response = client.models.generate_content(
            model="models/gemini-flash-lite-latest",
            contents=conversation.history + [
                {
                    "role": "user",
                    "parts": [{"text": prompt}]
                }
            ]
        )

        reply = response.text
        print("Gemini:", reply)

        # ---- SAVE CONVERSATION ----
        conversation.add_user_message(user_input)
        conversation.add_model_message(reply)

        time.sleep(0.5)

    except Exception as e:
        print("❌ Error:", e)

