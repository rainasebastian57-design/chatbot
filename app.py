from flask import Flask, render_template, request, jsonify
from google import genai

from config import GEMINI_API_KEY
from search import serpapi_search
from chat_store import ChatStore

app = Flask(__name__)

# Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)

# Multi-chat storage
store = ChatStore()


# -------- Helper functions --------

def needs_realtime_data(text):
    keywords = [
        "weather", "temperature", "price", "bitcoin",
        "today", "current", "news", "now"
    ]
    return any(k in text.lower() for k in keywords)


def extract_realtime_text(search_data):
    if not search_data:
        return "No real-time data found."

    if "answer_box" in search_data and search_data["answer_box"]:
        return str(search_data["answer_box"])

    organic = search_data.get("organic_results", [])
    if organic:
        return organic[0].get("snippet") or organic[0].get("title")

    return "No real-time data found."


# -------- Routes --------

@app.route("/")
def home():
    return render_template("index.html")


# Sidebar: list all chats
@app.route("/chats", methods=["GET"])
def list_chats():
    chats = store.list_chats()
    if not chats:
        store.create_chat("New chat")
        chats = store.list_chats()
    return jsonify({"chats": chats})


# Create new chat
@app.route("/chats", methods=["POST"])
def create_chat():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "New chat").strip()
    chat_id = store.create_chat(title)
    return jsonify({"id": chat_id})


# Load a specific chat
@app.route("/chats/<chat_id>", methods=["GET"])
def load_chat(chat_id):
    messages = store.get_messages(chat_id)
    if messages is None:
        return jsonify({"error": "Chat not found"}), 404
    return jsonify({"messages": messages})


# Send message to a chat
@app.route("/chats/<chat_id>/message", methods=["POST"])
def send_message(chat_id):
    data = request.get_json(silent=True) or {}
    user_text = (data.get("message") or "").strip()

    if not user_text:
        return jsonify({"reply": "Please enter a message."}), 400

    messages = store.get_messages(chat_id)
    if messages is None:
        return jsonify({"error": "Chat not found"}), 404

    prompt = user_text

    # Real-time data handling
    if needs_realtime_data(user_text):
        search_data = serpapi_search(user_text)
        realtime_info = extract_realtime_text(search_data)
        prompt = f"""
Use the following REAL-TIME information to answer accurately.
Do NOT hallucinate.

Real-time data:
{realtime_info}

User question:
{user_text}
"""

    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=messages + [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    )

    reply = response.text or "No reply generated."

    # Save conversation (store original user text)
    messages.append({"role": "user", "parts": [{"text": user_text}]})
    messages.append({"role": "model", "parts": [{"text": reply}]})
    store.save_messages(chat_id, messages)

    return jsonify({"reply": reply})


# Rename a chat
@app.route("/chats/<chat_id>/rename", methods=["POST"])
def rename_chat(chat_id):
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "Title required"}), 400

    ok = store.rename_chat(chat_id, title)
    return jsonify({"ok": ok})


# Delete a chat
@app.route("/chats/<chat_id>/delete", methods=["POST"])
def delete_chat(chat_id):
    store.delete_chat(chat_id)
    return jsonify({"ok": True})


# -------- Run server --------

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
