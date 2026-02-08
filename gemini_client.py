from google import genai

# Initialize Gemini client
client = genai.Client(api_key="AIzaSyA7yGmrvwKpGOofKzXX6rs3WEFr36NL30g")

def ask_gemini(conversation, user_input):
    # Add user message to memory
    conversation.add_user_message(user_input)

    # Call Gemini with Google Search grounding
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=conversation.get_history(),
        tools=[{"google_search": {}}]   # ✅ real-time Google Search
    )

    reply = response.text

    # Store Gemini response in memory
    conversation.add_model_message(reply)

    return reply
