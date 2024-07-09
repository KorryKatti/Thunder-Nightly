import customtkinter
import random

customtkinter.set_default_color_theme("themes/blue.json")



app = customtkinter.CTk()
app.title("Welcome To Thunder")
app.geometry("500x200")


def submit():
    username_text = username.get()
    email_text = email.get()
    print(f"User submitted username: {username_text}, email: {email_text}")

def no_login():
    print("Continuing without an account")


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
