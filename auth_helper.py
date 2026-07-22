import json
import os

USERS_FILE = "data/users.json"


# -----------------------------
# Create users.json if missing
# -----------------------------
def create_users_file():

    if not os.path.exists(USERS_FILE):

        with open(USERS_FILE, "w") as file:

            json.dump([], file, indent=4)


# -----------------------------
# Read all users
# -----------------------------
def get_users():

    create_users_file()

    with open(USERS_FILE, "r") as file:

        return json.load(file)


# -----------------------------
# Save all users
# -----------------------------
def save_users(users):

    with open(USERS_FILE, "w") as file:

        json.dump(users, file, indent=4)


# -----------------------------
# Register User
# -----------------------------
def register_user(name, email, password):

    users = get_users()

    for user in users:

        if user["email"].lower() == email.lower():

            return False

    users.append({

        "name": name,

        "email": email,

        "password": password,

        "vocabulary": [],

        "chat_history": [],

        "xp": 0,

        "level": 1,

        "streak": 0

    })

    save_users(users)

    return True


# -----------------------------
# Login User
# -----------------------------
def login_user(email, password):

    users = get_users()

    for user in users:

        if (
            user["email"].lower() == email.lower()
            and
            user["password"] == password
        ):

            return user

    return None