import os
import json
import time

from dotenv import load_dotenv
from google import genai


# ==========================
# Load API Key
# ==========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


if not API_KEY:
    raise Exception("GEMINI_API_KEY missing")


client = genai.Client(
    api_key=API_KEY
)



# ==========================
# Gemini Response Function
# ==========================

def get_ai_response(chat_history):


    user_message = chat_history[-1]["message"]


    prompt = f"""

You are Green Vocabulary AI.

Analyze the user's sentence.

Your tasks:

1. Rewrite the sentence using nature-inspired vocabulary.
2. Explain meaning.
3. Detect emotion.
4. Detect sentiment.
5. Provide green vocabulary learning.


User sentence:

{user_message}


Return ONLY valid JSON.

Use exactly this format:

{{
"rewrite":"",
"meaning":"",
"emotion":"",
"sentiment":"",
"green_word":"",
"word_meaning":"",
"eco_fact":"",
"eco_tip":"",
"sustainable_habit":"",
"challenge":""
}}

"""


    # Models in priority order

    models = [

        "gemini-flash-latest",

        "gemini-flash-lite-latest"

    ]



    for model in models:


        for attempt in range(3):


            try:


                print(
                    f"🤖 Trying {model} attempt {attempt+1}"
                )


                response = client.models.generate_content(

                    model=model,

                    contents=prompt

                )


                text = response.text.strip()



                # Remove markdown

                if "```json" in text:

                    text=text.replace(
                        "```json",
                        ""
                    )

                    text=text.replace(
                        "```",
                        ""
                    )


                result=json.loads(text)



                print(
                    f"✅ Gemini Success: {model}"
                )


                return result



            except Exception as e:


                print(
                    f"❌ {model} failed:",
                    e
                )


                time.sleep(2)




    # ==========================
    # Final Fallback
    # ==========================


    print(
        "🌿 Using Smart Fallback"
    )


    return {


        "rewrite":
        f"Your thought '{user_message}' can be expressed with a deeper connection to nature and sustainability.",


        "meaning":
        f"This sentence represents your feeling or idea: {user_message}",


        "emotion":
        "😊 Thoughtful",


        "sentiment":
        "Neutral",


        "green_word":
        "Resilience",


        "word_meaning":
        "The ability to adapt, recover and continue growing through challenges.",


        "eco_fact":
        "🌳 Plants and trees help maintain Earth's balance by absorbing carbon dioxide.",


        "eco_tip":
        "Take small sustainable actions every day to protect nature.",


        "sustainable_habit":
        "Reduce waste by choosing reusable products.",


        "challenge":
        "Try one eco-friendly habit today."

    }