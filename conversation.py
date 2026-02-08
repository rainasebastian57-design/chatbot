import json
import os

class Conversation:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = []
        self.load_history()

    def add_user_message(self, text):
        self.history.append({
            "role": "user",
            "parts": [{"text": text}]
        })
        self.save_history()

    def add_model_message(self, text):
        self.history.append({
            "role": "model",
            "parts": [{"text": text}]
        })
        self.save_history()

    def get_history(self):
        return self.history

    def save_history(self):
        with open(self.filename, "w") as f:
            json.dump(self.history, f, indent=2)

    def load_history(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.history = json.load(f)
        else:
            self.history = []
