import json

# ==========================
# Load Green Knowledge Base
# ==========================

with open("data/green_words.json", "r", encoding="utf-8") as file:
    green_words = json.load(file)


# ==========================
# Search Local Knowledge
# ==========================

def get_green_response(user_message):

    user_message = user_message.lower()

    for keyword in green_words:

        if keyword in user_message:

            print("✅ Local JSON Response Used")

            return green_words[keyword]

    print("❌ No Local Match Found")

    return None