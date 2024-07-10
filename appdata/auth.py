import customtkinter
import json
import time
import os
import uuid
import requests
from CTkMessagebox import CTkMessagebox

customtkinter.set_default_color_theme("themes/cyberpunk.json")

# Function to close window after a delay
def close_window(window):
    window.after(3000, window.destroy)  # Close window after 3000 milliseconds (3 seconds) and open main file
    os.system("python main.py") # TODO : review this file directory

# Function to generate a persistent identifier (UUID) for the user
def generate_user_id():
    if not os.path.exists('userdata'):
        os.makedirs('userdata')

    if os.path.exists('userdata/userid.txt'):
        with open('userdata/userid.txt', 'r') as file:
            user_id = file.read().strip()
    else:
        user_id = str(uuid.uuid4())
        with open('userdata/userid.txt', 'w') as file:
            file.write(user_id)
    return user_id

# Function to send user info to a server for cross-checking
def send_userinfo_to_server(username, email, user_id=None):
    url = 'http://127.0.0.1:5000/user'
    payload = {
        'username': username,
        'email': email
    }
    if user_id:
        payload['user_id'] = user_id

    try:
        response = requests.post(url, json=payload)
        server_response = response.json().get('status')

        if server_response == 231:
            CTkMessagebox(title="Login Success", message="User exists, logging in now", icon="check")
            close_window(app)
            return True
        elif server_response == 232:
            CTkMessagebox(title="Register Success", message="User does not exist, creating a new user", icon="check")
            close_window(app)
            return True
        elif server_response == 233:
            CTkMessagebox(title="Error", message="The email you provided didn't match the username", icon="warning")
            return False
        else:
            CTkMessagebox(title="Error", message="Some error occurred", icon="warning")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        CTkMessagebox(title="Error", message="Failed to connect to server", icon="warning")
        return False

# Create main application window
app = customtkinter.CTk()
app.title("Welcome To Thunder")
app.geometry("500x300")

def start_app():
    print("Starting app now")
    with open('userdata/userinfo.json', 'r') as file:
        user_data = json.load(file)
        send_userinfo_to_server(user_data['username'], user_data['email'])

def start_app_guest():
    print("Starting app with nothing to send to server")

def check_existing_user():
    if os.path.exists('userdata/userinfo.json'):
        CTkMessagebox(title="Welcome", message="Already logged in", icon="check")
        start_app()

def submit():
    username_text = username.get()
    email_text = email.get()
    if "@" not in email_text or "." not in email_text:
        CTkMessagebox(title="Error", message="The email you entered is incorrect", icon="warning")
        return

    user_id = generate_user_id()  # Get or generate persistent user identifier

    # Check if userinfo.json already exists
    if os.path.exists('userdata/userinfo.json'):
        with open('userdata/userinfo.json', 'r') as file:
            user_data = json.load(file)
            user_data['user_id'] = user_id  # Add user_id to existing data
    else:
        user_data = {
            "username": username_text,
            "email": email_text,
            "user_id": user_id  # Store user_id along with initial data
        }

    # Send user info to server first
    if send_userinfo_to_server(user_data['username'], user_data['email'], user_data['user_id']):
        if not os.path.exists('userdata'):
            os.makedirs('userdata')

        with open('userdata/userinfo.json', 'w') as file:
            json.dump(user_data, file)

        CTkMessagebox(title="Welcome", message="Welcome To Thunder", icon="check")
        close_window(app)

def no_login():
    user_id = generate_user_id()  # Get or generate persistent user identifier

    guest_data = {
        "username": "Guest",
        "email": "guest@thunder.korrykatti.site",
        "user_id": user_id  # Store user_id for guest user as well
    }

    if not os.path.exists('userdata'):
        os.makedirs('userdata')

    with open('userdata/userinfo.json', 'w') as file:
        json.dump(guest_data, file)

    CTkMessagebox(title="Welcome", message="Logging in with guest credentials", icon="check")
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
