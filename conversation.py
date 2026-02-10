import json
import os
from pathlib import Path

# Use the same BASE_DIR logic as your config.py
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

class Conversation:
    def __init__(self, chat_id, filename=None):
        # Create the data directory if it doesn't exist
        DATA_DIR.mkdir(exist_ok=True)
        
        # Use a unique filename per chat_id
        self.filename = DATA_DIR / f"{chat_id}.json"
        self.history = []
        self.load_history()

    def save_history(self):
        # Path objects work directly with open()
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=2)

    def load_history(self):
        if self.filename.exists():
            with open(self.filename, "r", encoding="utf-8") as f:
                self.history = json.load(f)
        else:
            self.history = []
