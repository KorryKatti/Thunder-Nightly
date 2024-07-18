import customtkinter
import json
import os
import uuid
import time
import requests

from CTkMessagebox import CTkMessagebox
from funx.fetch_data import fetch_server_stats, ping_server

# Set base URL for server
with open('userdata/settings.json', 'r') as f:
    settings = json.load(f)
    base_url = settings['server']

# Fetch server stats
stats = fetch_server_stats()
if stats:
    print(f"CPU Usage: {stats['cpu_usage']}%")
    print(f"Memory Usage: {stats['memory_usage']}%")
    print(f"Disk Usage: {stats['disk_usage']}%")

# Ping server
ping_response = ping_server()
if ping_response:
    print("Ping Response:", ping_response)

customtkinter.set_default_color_theme("themes/cyberpunk.json")

# Function to close window after a delay
def close_window(window):
    def destroy_and_launch():
        window.destroy()
        os.system("python newindex.py")  # Launch main file after window closes

    window.after(3000, destroy_and_launch)  # Close window after 3000 milliseconds (3 seconds)

# Function to save user data (username, email, user_id) locally
def save_user_data_locally(username, email, user_id):
    user_data = {
        "username": username,
        "email": email,
        "user_id": user_id
    }
    with open('userdata/userinfo.json', 'w') as file:
        json.dump(user_data, file)

# Create main application window
app = customtkinter.CTk()
app.title("Welcome To Thunder")
app.geometry("500x300")

def start_app():
    print("Starting app now")
    with open('userdata/userinfo.json', 'r') as file:
        user_data = json.load(file)
        if 'user_id' in user_data:
            CTkMessagebox(title="Welcome", message="Welcome To Thunder", icon="check")
            close_window(app)
        else:
            CTkMessagebox(title="Error", message="User ID not found locally", icon="warning")

def start_app_guest():
    print("Starting app with nothing to send to server")
    CTkMessagebox(title="Welcome", message="Logging in with guest credentials", icon="check")
    time.sleep(2)
    close_window(app)

def check_existing_user():
    if os.path.exists('userdata/userinfo.json'):
        with open('userdata/userinfo.json', 'r') as file:
            user_data = json.load(file)
            if 'user_id' in user_data:
                if user_data['username'] == "Guest":
                    start_app_guest()
                else:
                    start_app()

def submit():
    username_text = username.get()
    email_text = email.get()
    if "@" not in email_text or "." not in email_text:
        CTkMessagebox(title="Error", message="The email you entered is incorrect", icon="warning")
        return

    url = f'{base_url}/user'
    payload = {
        'username': username_text,
        'email': email_text
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()

        if response.status_code == 200:
            status = data.get('status')
            if status == 231 or status == 232:  # Login successful or user registered successfully
                user_id = data.get('user_id')
                save_user_data_locally(username_text, email_text, user_id)  # Save user data received from server
                CTkMessagebox(title="Welcome", message=data.get('message'), icon="check")
                close_window(app)
            elif status == 233:
                CTkMessagebox(title="Error", message="Invalid user credentials", icon="warning")
            else:
                CTkMessagebox(title="Error", message="Some error occurred", icon="warning")
        else:
            CTkMessagebox(title="Error", message="Failed to connect to server", icon="warning")

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        CTkMessagebox(title="Error", message="Failed to connect to server", icon="warning")

def no_login():
    user_id = str(uuid.uuid4())  # Generate a unique user ID for guest
    save_user_data_locally("Guest", "guest@thunder.korrykatti.site", user_id)

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
    close_window(app)

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
