import json
import os
from datetime import datetime

HISTORY_FILE = "data/quiz_history.json"


def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)


def save_attempt(sport, difficulty, score, total):

    history = load_history()

    history.append(
        {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "sport": sport,
            "difficulty": difficulty,
            "score": score,
            "total": total,
        }
    )

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)