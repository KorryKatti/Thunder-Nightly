#remaking the gui , to look better
import customtkinter 

#basic window which fits 800x640
app = customtkinter.CTk()
app.title("Thunder Client")
app.geometry("800x640")

# functions for apps

def homemenu(choice):
    print(choice)

def libmenu(choice):
    print(choice)

def commmenu(choice):
    print(choice)

def devmenu(choice):
    print(choice)

def cl_settings():
    print("settings pressed")

# the optionmenus on the top , not changing those for now

homemenu = customtkinter.CTkOptionMenu(app, values=["Home", "Client Update","Quit"], command=homemenu)
homemenu.grid(row=0, column=0, padx=5, pady=10)

libmenu = customtkinter.CTkOptionMenu(app, values=["Library","App Update"], command=libmenu)
libmenu.grid(row=0, column=1, padx=5, pady=10)

commmenu = customtkinter.CTkOptionMenu(app, values=["Community","Image Board","Thunder Halls"], command=commmenu)
commmenu.grid(row=0, column=2, padx=5, pady=10)

devmenu = customtkinter.CTkOptionMenu(app, values=["DevBlogs","Changelogs"], command=devmenu)
devmenu.grid(row=0, column=3, padx=5, pady=10)

settings = customtkinter.CTkButton(app, text="Settings", command=cl_settings)
settings.grid(row=0, column=4, padx=5, pady=10)














app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_columnconfigure(2, weight=1)
app.grid_columnconfigure(3, weight=1)
app.grid_columnconfigure(4, weight=1)


app.mainloop()