import os
import json
from dotenv import load_dotenv
from google import genai

# ==========================
# Load Environment Variables
# ==========================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise Exception("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ==========================
# Gemini AI Function
# ==========================

def get_ai_response(chat_history):

    # -------------------------
    # Build Conversation History
    # -------------------------

    history = ""

    for chat in chat_history:

        if chat["role"] == "user":
            history += f'User: {chat["message"]}\n'

        else:
            history += f'Assistant: {chat["message"]}\n'

    prompt = f"""
You are Green Vocabulary AI.

You are an intelligent and friendly environmental chatbot.

Use the previous conversation to understand context.

Conversation History:

{history}

Return ONLY valid JSON.

Do NOT use markdown.

Return this exact JSON structure:

{{
    "emotion":"",
    "sentiment":"",
    "rewrite":"",
    "meaning":"",
    "eco_fact":"",
    "green_word":"",
    "word_meaning":"",
    "eco_tip":"",
    "sustainable_habit":"",
    "challenge":""
}}

Rules:

1. Remember previous conversation.
2. If the user says:
   - Explain again
   - Continue
   - Tell me more
   - Another example
   - Why?
   then continue naturally.
3. Detect emotion.
4. Detect sentiment.
5. Rewrite the sentence using nature-inspired vocabulary.
6. Teach one green vocabulary word.
7. Give one eco fact.
8. Give one eco tip.
9. Suggest one sustainable habit.
10. Give one eco challenge.
11. Keep answers short, friendly, and encouraging.
"""

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        text = response.text.strip()

        # Remove markdown if Gemini adds it
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        print("\n========== Gemini Response ==========")
        print(text)
        print("=====================================\n")

        return json.loads(text)

    except json.JSONDecodeError:

        print("JSON Parsing Error")

        return {
            "emotion": "Neutral",
            "sentiment": "Neutral",
            "rewrite": "I generated a response, but couldn't understand its format. Please try again.",
            "meaning": "",
            "eco_fact": "Trees help reduce air pollution.",
            "green_word": "Ecosystem",
            "word_meaning": "A community of living organisms interacting with their environment.",
            "eco_tip": "Plant a tree whenever possible.",
            "sustainable_habit": "Use reusable shopping bags.",
            "challenge": "Avoid using plastic bags today."
        }

    except Exception as e:

        print("Gemini Error:", e)

        return {
            "emotion": "😊 Calm",
            "sentiment": "Neutral",
            "rewrite": "⚠️ Gemini AI is temporarily unavailable because the service is experiencing high demand. Please try again in a few moments.",
            "meaning": "Your chatbot is still running correctly.",
            "eco_fact": "Did you know? A mature tree can absorb around 22 kg of carbon dioxide each year.",
            "green_word": "Resilience",
            "word_meaning": "The ability to recover and continue despite challenges.",
            "eco_tip": "Try asking your question again after a few moments.",
            "sustainable_habit": "Carry a reusable water bottle to reduce plastic waste.",
            "challenge": "Today, avoid using one single-use plastic item."
        }