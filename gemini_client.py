from google import genai

from config import GEMINI_API_KEY

# Initialize Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

def ask_gemini(conversation, user_input):
    conversation.add_user_message(user_input)

    response = client.models.generate_content(
        model="gemini-2.0-flash", # Fixed model name
        contents=conversation.get_history(),
        config={"tools": [{"google_search": {}}]} # Updated syntax for SDK
    )

    # Use getattr or a simple if-check to prevent crashes
    reply = response.text if response.text else "I'm sorry, I couldn't generate a response."
    
    conversation.add_model_message(reply)
    return reply

    