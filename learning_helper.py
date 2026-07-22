import json
import os

HISTORY_FILE = "data/vocabulary_history.json"


# -----------------------------
# Create history file if missing
# -----------------------------
def initialize_history():

    if not os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "w") as file:
            json.dump([], file, indent=4)


# -----------------------------
# Save vocabulary
# -----------------------------
def save_word(word, meaning):

    initialize_history()

    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)

    # Don't save duplicates
    for item in history:

        if item["word"].lower() == word.lower():
            return

    history.append({
        "word": word,
        "meaning": meaning
    })

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


# -----------------------------
# Read history
# -----------------------------
def get_history():

    initialize_history()

    with open(HISTORY_FILE, "r") as file:
        return json.load(file)