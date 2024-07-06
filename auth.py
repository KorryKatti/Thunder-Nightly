import customtkinter

customtkinter.set_default_color_theme("themes/cyberpunk.json")


app = customtkinter.CTk()
app.title("Welcome To Thunder")
app.geometry("500x200")


def submit():
    username_text = username.get()
    email_text = email.get()
    print(f"User submitted username: {username_text}, email: {email_text}")


title = customtkinter.CTkLabel(app, text="Login Or Register", font=("Roboto", 14))
title.grid(row=0, column=0, padx=20, pady=10)

username = customtkinter.CTkEntry(app, placeholder_text="Enter Username")
username.grid(row=1, column=0, padx=20, pady=10)

email = customtkinter.CTkEntry(app, placeholder_text="Enter Email")
email.grid(row=2, column=0, padx=20, pady=10)

submit_button = customtkinter.CTkButton(app, text="Submit", command=submit)
submit_button.grid(row=3, column=0, padx=20, pady=10)


app.grid_columnconfigure(0, weight=1)


app.mainloop()
