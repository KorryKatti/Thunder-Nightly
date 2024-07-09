import customtkinter
import random
import string
import json
import os
from CTkMessagebox import CTkMessagebox
import requests

customtkinter.set_default_color_theme("themes/cyberpunk.json")

def close_window(window):
    window.destroy()

def reopen_app():
    app.deiconify()

# Function to send user info to a server for cross-checking
def send_userinfo_to_server(username, email, secret_key):
    url = 'http://127.0.0.1:5000/user'
    payload = {
        'username': username,
        'email': email,
        'secret_key': secret_key
    }
    response = requests.post(url, json=payload)
    server_response = response.json().get('status')

    if server_response == 231:
        CTkMessagebox(title="Login Success", message="User exists, logging in now", icon="check")
        close_window(app)
    elif server_response == 232:
        CTkMessagebox(title="Register Success", message="User does not exist, creating a new user", icon="check")
        close_window(app)
    elif server_response == 233:
        CTkMessagebox(title="Error", message="The email you provided didn't match the username", icon="warning")
        reopen_app()
    else:
        CTkMessagebox(title="Error", message="Some error occurred", icon="error")
        reopen_app()

# Create main application window
app = customtkinter.CTk()
app.title("Welcome To Thunder")
app.geometry("500x300")

def start_app():
    print("Starting app now")
    with open('userdata/userinfo.json', 'r') as file:
        user_data = json.load(file)
        send_userinfo_to_server(user_data['username'], user_data['email'], user_data['secret_key'])

def start_app_guest():
    print("Starting app with nothing to send to server")

def check_existing_user():
    if os.path.exists('userdata/userinfo.json'):
        CTkMessagebox(title="Welcome", message="Already logged in", icon="check")
        start_app()

def generate_secret_key(length=8):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def submit():
    username_text = username.get()
    email_text = email.get()
    if "@" not in email_text or "." not in email_text:
        CTkMessagebox(title="Error", message="The email you entered is incorrect", icon="warning")
        return
    random_string = generate_secret_key()
    user_data = {
        "username": username_text,
        "email": email_text,
        "secret_key": random_string
    }
    if not os.path.exists('userdata'):
        os.makedirs('userdata')
    with open('userdata/userinfo.json', 'w') as file:
        json.dump(user_data, file)
    CTkMessagebox(title="Welcome", message="Welcome To Thunder", icon="check")
    close_window(app)
    start_app()

def no_login():
    random_string = generate_secret_key()
    guest_data = {
        "username": "Guest",
        "email": "guest@thunder.korrykatti.site",
        "secret_key": random_string
    }
    if not os.path.exists('userdata'):
        os.makedirs('userdata')
    with open('userdata/userinfo.json', 'w') as file:
        json.dump(guest_data, file)
    CTkMessagebox(title="Welcome", message="Logging in with guest credentials", icon="check")
    close_window(app)
    start_app_guest()

# UI Elements
title = customtkinter.CTkLabel(app, text="Login or Register", font=("Roboto", 14))
title.grid(row=0, column=0, padx=20, pady=5)

username = customtkinter.CTkEntry(app, placeholder_text="Enter Username")
username.grid(row=1, column=0, padx=20, pady=5)

email = customtkinter.CTkEntry(app, placeholder_text="Enter Email")
email.grid(row=2, column=0, padx=20, pady=5)

submit_button = customtkinter.CTkButton(app, text="Submit", command=submit)
submit_button.grid(row=3, column=0, padx=20, pady=10)

optional_button = customtkinter.CTkButton(app, text="Continue without an account", command=no_login)
optional_button.grid(row=4, column=0, padx=20, pady=5)

app.grid_columnconfigure(0, weight=1)

# Check for existing user data on startup
check_existing_user()

app.mainloop()
