from flask import session
from datetime import datetime
from database import get_connection
import json



def save_chat(user_message, ai_response):


    if "user_id" not in session:

        return



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """

        INSERT INTO chats

        (
            user_id,
            user_message,
            bot_response,
            created_at
        )

        VALUES (?,?,?,?)

        """,

        (

            session["user_id"],

            user_message,

            json.dumps(ai_response),

            datetime.now()

        )

    )



    connection.commit()

    connection.close()




def get_user_chats():


    if "user_id" not in session:

        return []



    connection = get_connection()

    cursor = connection.cursor()



    cursor.execute(

        """

        SELECT *

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



    return chats