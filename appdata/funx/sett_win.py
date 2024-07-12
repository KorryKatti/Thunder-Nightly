import customtkinter
import requests
import json
import os



# from ../userdata/settings.json get theme name , theme is at ../themes/{themename}.json
# get themename from settings.json
with open("../userdata/settings.json", "r") as f:
    settings = json.load(f)
    themename = settings["theme"]
    print(themename)
    them_file = "../themes/" + themename + ".json"
    print(them_file)
    customtkinter.set_default_color_theme(them_file)

app = customtkinter.CTk()
app.geometry("600x500")
app.title("Settings For Thunder")

def download_theme():
    print("Downloading theme...")
    theme_url = theme_url.get()  # Assuming theme_url is an Entry widget in your GUI
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


# Functions for button commands
def theme_button():
    print("Changing theme...")
    clear_widgets()
    them_title = customtkinter.CTkLabel(s_frame, text="Theme Settings", font=("Arial", 20))
    them_title.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    them_subtitle = customtkinter.CTkLabel(s_frame, text="Select a theme or download or make a new one:", font=("Arial", 14))
    them_subtitle.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    theme_url = customtkinter.CTkEntry(s_frame,placeholder_text="Insert url for theme if you want to download it from a url ( must end in .json)")
    theme_url.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
    theme_download = customtkinter.CTkButton(s_frame, text="Download Theme", command=download_theme)
    theme_download.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        # display existing themes
    them_directory = "../themes"
    files = os.listdir(them_directory)
    json_file_count = 0
    for file in files:
        if file.endswith('.json'):
            json_file_count += 1
    print(json_file_count)
    for i in range(json_file_count):
        theme_butt = customtkinter.CTkButton(s_frame, text=files[i], command=lambda f=files[i]: from_preset(f))
        theme_butt.grid(row=i+4, column=0, padx=10, pady=10, sticky="ew")


def from_preset(theme_name):
    print(theme_name)

def signout_button():
    print("Signing out...")  # Placeholder for sign out functionality
    clear_widgets()

def setserver_button():
    print("Setting server...")  # Placeholder for setting server functionality
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

# function to clear widgets in s_frame
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
"""

textbox = customtkinter.CTkTextbox(s_frame)
textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
textbox.insert("0.0", friendly_text)
textbox.configure(state="disabled")  # make the textbox read-only
s_frame.grid_columnconfigure(0, weight=1)

# Start the application loop
app.mainloop()
