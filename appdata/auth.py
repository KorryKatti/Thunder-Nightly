import customtkinter
import random
import string
import json
from CTkMessagebox import CTkMessagebox

customtkinter.set_default_color_theme("themes/cyberpunk.json")

def close_window(window):
    window.destroy()

app = customtkinter.CTk()
app.title("Welcome To Thunder")
app.geometry("500x200")


def start_app():
    print("Starting app now")

# check for existing userdata/userinfo.json
if os.path.exists('userdata/userinfo.json'):
    CTkMessagebox(title="Welcome", message="Already logged in", icon="check")
    start_app()

def generate_secret_key(length=8):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for i in range(length))
    return random_string

def submit():
    username_text = username.get()
    email_text = email.get()
    # check if valid email or not, if not show popup asking for right email format
    if "@" not in email_text or "." not in email_text:
        print("Invalid email format")
        #message box asking user to enter correct email format
        CTkMessagebox(title="Error", message="The Email You Entered Was Incorrect", icon="warning")
        return
    else:
        print(f"User submitted username: {username_text}, email: {email_text}")
        random_string = generate_secret_key()
        print(f"Generate secret key for user {username_text}: {random_string}")
        # save username , email and secrety key in userdata/userinfo.json
        with open('userdata/userinfo.json', 'w') as file:
            data = {
                "username": username_text,
                "email": email_text,
                "secret_key": random_string
            }
            json.dump(data, file)
        CTkMessagebox(title="Welcome", message="Welcome To Thunder", icon="check")
        app.after(3000, close_window, app)
        start_app()

   
def no_login():
    print("Continuing without an account")
    random_string = generate_secret_key()
    # print(f"Random alphanumeric string: {random_string}")
    # save guest username , guest email and secret key in userdata/userinfo.json
    with open('userdata/userinfo.json','w') as file:
        data = {
            "username": "Guest",
            "email": "guest@thunder.korrykatti.site",
            "secret_key": random_string
        }
        json.dump(data, file)
    CTkMessagebox(title="Welcome", message="Welcome To Thunder. Logging in with guest credentials now", icon="check")
    app.after(3000, close_window, app)
    start_app()
    


title = customtkinter.CTkLabel(app, text="Login Or Register", font=("Roboto", 14))
title.grid(row=0, column=0, padx=20, pady=5)

username = customtkinter.CTkEntry(app, placeholder_text="Enter Username")
username.grid(row=1, column=0, padx=20, pady=5)

email = customtkinter.CTkEntry(app, placeholder_text="Enter Email")
email.grid(row=2, column=0, padx=20, pady=5)

submit_button = customtkinter.CTkButton(app, text="Submit", command=submit)
submit_button.grid(row=3, column=0, padx=20, pady=10)

optional_button = customtkinter.CTkButton(app, text="Continue without an account", command=no_login)
optional_button.grid(row=4,column=0, padx=20, pady=5)


app.grid_columnconfigure(0, weight=1)


app.mainloop()
