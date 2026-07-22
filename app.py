from flask import Flask, render_template, request, jsonify, session, redirect
import json
import bcrypt
from datetime import timedelta

from database import get_connection

from gemini_helper import get_ai_response
from green_helper import get_green_response
from learning_helper import save_word, get_history

from chat_history_helper import (
    save_chat,
    get_user_chats
)


app = Flask(__name__)

app.secret_key = "green_vocabulary_secret_key"
app.permanent_session_lifetime = timedelta(minutes=30)
from datetime import timedelta



# ==========================
# Memory
# ==========================

chat_history = []

last_ai_response = {}



# ==========================
# Home Page
# ==========================

@app.route("/")
def home():

    if "user_id" not in session:

        return redirect("/login")


    response = render_template("index.html")


    session.pop("old_message", None)

    session.pop("old_response", None)


    return response

    if "user_id" not in session:

        return redirect("/login")


    return render_template("index.html")



# ==========================
# Vocabulary History
# ==========================

@app.route("/history")
def history():

    return jsonify(get_history())



# ==========================
# Chat History
# ==========================

@app.route("/chat-history")
def chat_history_api():

    if "user_id" not in session:

        return jsonify({

            "success": False,

            "message": "User not logged in"

        })


    chats = get_user_chats()


    chat_list = []


    for chat in chats:

        chat_list.append({

            "id": chat["id"],

            "message": chat["user_message"],

            "response": chat["bot_response"],

            "time": chat["created_at"]

        })


    return jsonify({

        "success": True,

        "chats": chat_list

    })



@app.route("/delete-chat/<int:chat_id>", methods=["DELETE"])
def delete_user_chat(chat_id):

    if "user_id" not in session:

        return jsonify({

            "success":False,

            "message":"Not logged in"

        })


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(

        """

        DELETE FROM chats

        WHERE id=? AND user_id=?

        """,

        (

            chat_id,

            session["user_id"]

        )

    )


    connection.commit()

    connection.close()


    return jsonify({

        "success":True

    })

def chat_history_api():

    if "user_id" not in session:

        return jsonify({

            "success": False,

            "message": "User not logged in"

        })


    chats = get_user_chats()


    chat_list = []


    for chat in chats:

        chat_list.append({

            "id": chat["id"],

            "message": chat["user_message"],

            "response": chat["bot_response"],

            "time": chat["created_at"]

        })


    return jsonify({

        "success": True,

        "chats": chat_list

    })

@app.route("/continue-chat/<int:chat_id>")
def continue_chat(chat_id):

    if "user_id" not in session:

        return redirect("/login")


    connection = get_connection()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM chats
        WHERE id=? AND user_id=?
        """,
        (
            chat_id,
            session["user_id"]
        )
    )


    chat = cursor.fetchone()


    connection.close()


    if chat:

        session["old_message"] = chat["user_message"]

        session["old_response"] = chat["bot_response"]


    return redirect("/")

# ==========================
# Chat API
# ==========================

@app.route("/chat", methods=["POST"])
def chat():

    global last_ai_response


    data = request.get_json()


    user_message = data["message"].strip()


    lower_message = user_message.lower()



    # ==========================
    # Smart Memory
    # ==========================


    if "challenge" in lower_message and last_ai_response:


        save_chat(user_message, last_ai_response)


        return jsonify({

            "emotion": last_ai_response.get("emotion",""),

            "sentiment": last_ai_response.get("sentiment",""),

            "rewrite": "Here is your previous eco challenge.",

            "meaning": "",

            "eco_fact": "",

            "green_word": "",

            "word_meaning": "",

            "eco_tip": "",

            "sustainable_habit": "",

            "challenge": last_ai_response.get("challenge","")

        })



    if ("green word" in lower_message or "vocabulary" in lower_message) and last_ai_response:


        save_chat(user_message, last_ai_response)


        return jsonify({

            "emotion": last_ai_response.get("emotion",""),

            "sentiment": last_ai_response.get("sentiment",""),

            "rewrite": "Here is the previous green vocabulary.",

            "meaning": "",

            "eco_fact": "",

            "green_word": last_ai_response.get("green_word",""),

            "word_meaning": last_ai_response.get("word_meaning",""),

            "eco_tip": "",

            "sustainable_habit": "",

            "challenge": ""

        })



    if ("eco fact" in lower_message or "fact" in lower_message) and last_ai_response:


        save_chat(user_message,last_ai_response)


        return jsonify({

            "emotion": last_ai_response.get("emotion",""),

            "sentiment": last_ai_response.get("sentiment",""),

            "rewrite": "Here is the previous eco fact.",

            "meaning": "",

            "eco_fact": last_ai_response.get("eco_fact",""),

            "green_word": "",

            "word_meaning": "",

            "eco_tip": "",

            "sustainable_habit": "",

            "challenge": ""

        })



    if ("eco tip" in lower_message or "tip" in lower_message) and last_ai_response:


        save_chat(user_message,last_ai_response)


        return jsonify({

            "emotion": last_ai_response.get("emotion",""),

            "sentiment": last_ai_response.get("sentiment",""),

            "rewrite": "Here is the previous eco tip.",

            "meaning": "",

            "eco_fact": "",

            "green_word": "",

            "word_meaning": "",

            "eco_tip": last_ai_response.get("eco_tip",""),

            "sustainable_habit": "",

            "challenge": ""

        })



    if "habit" in lower_message and last_ai_response:


        save_chat(user_message,last_ai_response)


        return jsonify({

            "emotion": last_ai_response.get("emotion",""),

            "sentiment": last_ai_response.get("sentiment",""),

            "rewrite": "Here is the previous sustainable habit.",

            "meaning": "",

            "eco_fact": "",

            "green_word": "",

            "word_meaning": "",

            "eco_tip": "",

            "sustainable_habit": last_ai_response.get("sustainable_habit",""),

            "challenge": ""

        })



    # ==========================
    # Local JSON AI
    # ==========================


    local_response = get_green_response(user_message)



    if local_response:


        print("🌿 Responded from Local JSON")


        last_ai_response = local_response


        if local_response.get("green_word"):


            save_word(

                local_response["green_word"],

                local_response["word_meaning"]

            )



        save_chat(user_message,local_response)


        return jsonify(local_response)




    # ==========================
    # Gemini AI
    # ==========================


    print("🤖 Responded from Gemini AI")



    chat_history.append({

        "role":"user",

        "message":user_message

    })



    if len(chat_history)>10:

        chat_history.pop(0)



    ai_response = get_ai_response(chat_history)



    last_ai_response = ai_response



    if ai_response.get("green_word"):


        save_word(

            ai_response["green_word"],

            ai_response["word_meaning"]

        )



    save_chat(user_message,ai_response)



    chat_history.append({

        "role":"assistant",

        "message":ai_response["rewrite"]

    })



    if len(chat_history)>10:

        chat_history.pop(0)



    return jsonify(ai_response)
# ==========================
# Signup Page
# ==========================

@app.route("/signup")
def signup_page():

    return render_template("signup.html")



# ==========================
# Login Page
# ==========================

@app.route("/login")
def login_page():

    return render_template("login.html")



# ==========================
# Signup API
# ==========================

@app.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()


    name = data.get("name")

    email = data.get("email")

    password = data.get("password")



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        "SELECT * FROM users WHERE email=?",

        (email,)

    )



    existing_user = cursor.fetchone()



    if existing_user:


        connection.close()


        return jsonify({

            "success":False,

            "message":"Email already registered"

        })



    hashed_password = bcrypt.hashpw(

        password.encode("utf-8"),

        bcrypt.gensalt()

    )



    cursor.execute(

        """

        INSERT INTO users

        (name,email,password)

        VALUES (?,?,?)

        """,

        (

            name,

            email,

            hashed_password.decode("utf-8")

        )

    )



    connection.commit()

    connection.close()



    return jsonify({

        "success":True,

        "message":"Account created"

    })




# ==========================
# Login API
# ==========================

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()



    email = data.get("email")

    password = data.get("password")



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """

        SELECT *

        FROM users

        WHERE email=?

        """,

        (

            email,

        )

    )



    user = cursor.fetchone()



    connection.close()



    if user:


        stored_password = user["password"].encode("utf-8")



        if bcrypt.checkpw(

            password.encode("utf-8"),

            stored_password

        ):



            

            session.permanent = False

            session["user_id"] = user["id"]

            session["user_name"] = user["name"]


            return jsonify({

                "success":True,

                "message":"Login successful"

            })



    return jsonify({

        "success":False,

        "message":"Invalid email or password"

    })
# ==========================
# Count Vocabulary Words
# ==========================

def get_user_word_count():

    try:

        with open(
            "data/vocabulary_history.json",
            "r"
        ) as file:

            words = json.load(file)


        return len(words)


    except:

        return 0









# ==========================
# Dashboard Data API
# ==========================

@app.route("/dashboard-data")
def dashboard_data():


    if "user_id" not in session:

        return jsonify({

            "success":False

        })



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """

        SELECT COUNT(*)

        FROM chats

        WHERE user_id=?

        """,

        (

            session["user_id"],

        )

    )


    total_chats = cursor.fetchone()[0]



    cursor.execute(

        """

        SELECT

        user_message,

        bot_response

        FROM chats

        WHERE user_id=?

        ORDER BY id DESC

        LIMIT 5

        """,

        (

            session["user_id"],

        )

    )



    chats = cursor.fetchall()



    connection.close()



    chat_list = []



    for chat in chats:


        chat_list.append({

            "message":chat["user_message"],

            "response":chat["bot_response"]

        })



    return jsonify({

        "success":True,

        "name":session["user_name"],

        "total_chats":total_chats,

        "total_words":get_user_word_count(),

        "chats":chat_list

    })





# ==========================
# Logout
# ==========================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")





# ==========================
# Personal Chat History
# ==========================

@app.route("/my-chats")
def my_chats():


    if "user_id" not in session:

        return jsonify({

            "success":False,

            "message":"User not logged in"

        })



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """

        SELECT

        id,

        user_message,

        bot_response,

        created_at


        FROM chats


        WHERE user_id=?


        ORDER BY id DESC


        """,

        (

            session["user_id"],

        )

    )



    chats = cursor.fetchall()



    connection.close()



    chat_list = []



    for chat in chats:


        chat_list.append({

            "id":chat["id"],

            "message":chat["user_message"],

            "response":chat["bot_response"],

            "time":chat["created_at"]

        })



    return jsonify({

        "success":True,

        "chats":chat_list

    })

# ==========================
# Dashboard Page
# ==========================

@app.route("/dashboard")
def dashboard():


    if "user_id" not in session:

        return redirect("/login")


    return render_template("dashboard.html")



# ==========================
# Chat History Page
# ==========================

@app.route("/chat-history-page")
def chat_history_page():

    if "user_id" not in session:

        return redirect("/login")


    return render_template("chat_history.html")

# ==========================
# Run Application
# ==========================

if __name__ == "__main__":

    app.run(debug=True)
    
    