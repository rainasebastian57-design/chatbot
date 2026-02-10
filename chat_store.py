import json
import os
import uuid
from datetime import datetime
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent


DATA_DIR = BASE_DIR / "data"
CHATS_DIR = DATA_DIR / "chats"
INDEX_FILE = DATA_DIR / "chats_index.json"



def _now():
    return datetime.now().isoformat(timespec="seconds")


class ChatStore:
    def __init__(self):
        os.makedirs(CHATS_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        if not os.path.exists(INDEX_FILE):
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    def _read_index(self):
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def _write_index(self, items):
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2)

    def list_chats(self):
        chats = self._read_index()
        return sorted(chats, key=lambda x: x.get("updated_at", ""), reverse=True)

    def create_chat(self, title="New chat"):
        chat_id = str(uuid.uuid4())
        chat_path = os.path.join(CHATS_DIR, f"{chat_id}.json")

        with open(chat_path, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2)

        index = self._read_index()
        index.append({
            "id": chat_id,
            "title": title,
            "created_at": _now(),
            "updated_at": _now()
        })
        self._write_index(index)
        return chat_id

    def get_messages(self, chat_id):
        chat_path = os.path.join(CHATS_DIR, f"{chat_id}.json")
        if not os.path.exists(chat_path):
            return None
        with open(chat_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_messages(self, chat_id, messages):
        chat_path = os.path.join(CHATS_DIR, f"{chat_id}.json")
        with open(chat_path, "w", encoding="utf-8") as f:
            json.dump(messages, f, indent=2)

        index = self._read_index()
        for item in index:
            if item["id"] == chat_id:
                item["updated_at"] = _now()
                break
        self._write_index(index)

    def rename_chat(self, chat_id, title):
        index = self._read_index()
        for item in index:
            if item["id"] == chat_id:
                item["title"] = title
                item["updated_at"] = _now()
                self._write_index(index)
                return True
        return False

    def delete_chat(self, chat_id):
        chat_path = os.path.join(CHATS_DIR, f"{chat_id}.json")
        if os.path.exists(chat_path):
            os.remove(chat_path)

        index = [x for x in self._read_index() if x.get("id") != chat_id]
        self._write_index(index)
        return True

