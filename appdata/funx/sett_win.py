import customtkinter
import requests
import json
import os
import random

# Load initial theme and server from settings.json
with open("../userdata/settings.json", "r") as f:
    settings = json.load(f)
    initial_theme = settings.get("theme", "default_theme.json")
    initial_server = settings.get("server", "127.0.0.1:5000")
    print(f"Initial theme: {initial_theme}")
    print(f"Initial server: {initial_server}")

    if initial_theme.endswith(".json"):
        themename = initial_theme[:-5]  # Remove ".json" as it exists in the setting
    else:
        themename = initial_theme
    them_file = f"../themes/{themename}.json"
    print(f"Theme file: {them_file}")
    customtkinter.set_default_color_theme(them_file)

app = customtkinter.CTk()
app.geometry("600x500")
app.title("Settings For Thunder")

def download_theme(theme_url_entry):
    print("Downloading theme...")
    theme_url = theme_url_entry.get()
    if not theme_url.endswith(".json"):
        print("Theme URL must end in .json")
        return
    else:
        try:
            # Extract filename from the URL
            filename = os.path.basename(theme_url)

            # Download theme to ../themes
            response = requests.get(theme_url)
            if response.status_code == 200:
                with open(f"../themes/{filename}", "wb") as f:
                    f.write(response.content)
                print(f"Theme downloaded successfully as {filename}!")
            else:
                print("Failed to download theme.")
        except Exception as e:
            print(f"Error downloading theme: {e}")

def theme_button():
    print("Changing theme...")
    clear_widgets()
    them_title = customtkinter.CTkLabel(s_frame, text="Theme Settings", font=("Arial", 20))
    them_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    them_subtitle = customtkinter.CTkLabel(s_frame, text="Select a theme or download or make a new one:", font=("Arial", 14))
    them_subtitle.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    theme_url_entry = customtkinter.CTkEntry(s_frame, placeholder_text="Insert URL for theme ending in .json")
    theme_url_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    theme_download = customtkinter.CTkButton(s_frame, text="Download Theme", command=lambda: download_theme(theme_url_entry))
    theme_download.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
    # Display existing themes
    them_directory = "../themes"
    files = os.listdir(them_directory)
    json_file_count = sum(1 for file in files if file.endswith('.json'))
    print(json_file_count)
    direction = random.choice(["e", "w"])  # randomly choose 'e' or 'w'
    for i, file in enumerate(files):
        if file.endswith('.json'):
            theme_butt = customtkinter.CTkButton(s_frame, text=file, command=lambda f=file: from_preset(f))
            theme_butt.grid(row=i+4, column=0, padx=10, pady=10, sticky=f"{direction}")

def from_preset(theme_name):
    print(theme_name)
    with open("../userdata/settings.json", "w") as f:
        settings["theme"] = theme_name
        json.dump(settings, f)
        print("Theme set to " + theme_name)
        customtkinter.set_default_color_theme(f"../themes/{theme_name}")

def setserver_button():
    print("Setting server...")
    clear_widgets()
    server_title = customtkinter.CTkLabel(s_frame, text="Server Settings", font=("Arial", 20))
    server_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    server_subtitle = customtkinter.CTkLabel(s_frame, text="Enter the URL for the server:", font=("Arial", 14))
    server_subtitle.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    server_url_entry = customtkinter.CTkEntry(s_frame, placeholder_text="Insert URL for server")
    server_url_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    server_save_button = customtkinter.CTkButton(s_frame, text="Save Server URL", command=lambda: save_server_url(server_url_entry))
    server_save_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
    server_url_entry.insert(0, initial_server)
    server_warning = """

Warning: Changing Server Settings

Changing server settings can affect how Thunder interacts with external services. Please ensure that you have the correct server information before making changes. Incorrect settings may result in connection issues or data loss.

Important Note: Using third-party servers, especially those you do not trust, can pose risks such as potential data exposure. It is recommended to use official servers or your own server to maintain data security.

---

Default Server Options

In case you need to revert changes, here are two default server options:

- Default Server 1: 127.0.0.1:5000
- Default Server 2: example.com:8080

These options are provided for your convenience in case you encounter issues with server settings. Always ensure the server you use is reliable and secure.
    """
    serv_warn = customtkinter.CTkTextbox(s_frame)
    serv_warn.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    serv_warn.insert("0.0", server_warning)
    serv_warn.configure(state="disabled")  # make the textbox read-only
def save_server_url(server_url_entry):
    new_server_url = server_url_entry.get()
    print(f"Saving server URL: {new_server_url}")
    with open("../userdata/settings.json", "w") as f:
        settings["server"] = new_server_url
        json.dump(settings, f)
        print("Server URL set to " + new_server_url)

def signout_button():
    print("Signing out...")  # Placeholder for sign out functionality
    clear_widgets()

def fetchuser_button():
    print("Fetching user data...")  # Placeholder for fetching user data functionality
    clear_widgets()

def app_manager_button():
    print("Opening app manager...")  # Placeholder for app manager functionality
    clear_widgets()

# Main frame and layout
op_frame = customtkinter.CTkScrollableFrame(app)
op_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

s_frame = customtkinter.CTkScrollableFrame(app)
s_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

# Function to clear widgets in s_frame
def clear_widgets():
    for widget in s_frame.winfo_children():
        widget.destroy()

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=100)
app.grid_rowconfigure(0, weight=1)

# Buttons for operations
theme_button = customtkinter.CTkButton(op_frame, text="Change Theme", command=theme_button)
theme_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

signout_button = customtkinter.CTkButton(op_frame, text="Sign Out", command=signout_button)
signout_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

setserver_button = customtkinter.CTkButton(op_frame, text="Set Server", command=setserver_button)
setserver_button.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

fetchuser_button = customtkinter.CTkButton(op_frame, text="Fetch User Data", command=fetchuser_button)
fetchuser_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

app_manager_button = customtkinter.CTkButton(op_frame, text="App Manager", command=app_manager_button)
app_manager_button.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

# Friendly instructions and tips in a textbox
friendly_text = """
Hello User! Welcome to Thunder settings. Here, you can customize your experience and manage your preferences.
Feel free to explore and make adjustments as needed.

Please be cautious while making changes. Although the settings are designed to enhance your experience,
downloading unverified themes or setting up external servers can potentially impact performance or security.

If you encounter any issues or need assistance, don't hesitate to contact our support team.
We're here to help you get the most out of Thunder!

Note :
All settings are applied on restarting the client with a few exceptions.

Thank you for using Thunder!

All your settings are in ../userdata/settings.json in case you mess up and app doesn't start.
"""
textbox = customtkinter.CTkTextbox(s_frame, width=80, height=275)
textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
textbox.insert("0.0", friendly_text)
textbox.configure(state="disabled")  # make the textbox read-only
s_frame.grid_columnconfigure(0, weight=1)
s_frame.grid_rowconfigure(0, weight=1)


# Start the application loop
app.mainloop()
