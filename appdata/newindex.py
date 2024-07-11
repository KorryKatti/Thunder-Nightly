import customtkinter
from PIL import Image as PILImage
from PIL import ImageTk
from PIL import Image
import json
from funx.fetch_data import fetch_server_stats, ping_server

# import server stats
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


# import user data
file_path = 'userdata/userinfo.json'
with open(file_path, 'r') as file:
    data = json.load(file)
username = data['username']
print(f"Username: {username}")


# Basic window which fits 800x640
app = customtkinter.CTk()
app.title("Thunder Client")
app.geometry("1024x640")

# Functions for apps
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

def launch_mirage():
    print("launching mirage")

# The option menus on the top
homemenu = customtkinter.CTkOptionMenu(app, values=["Home", "Client Update", "Quit"], command=homemenu)
homemenu.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

libmenu = customtkinter.CTkOptionMenu(app, values=["Library", "App Update"], command=libmenu)
libmenu.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

commmenu = customtkinter.CTkOptionMenu(app, values=["Community", "Image Board", "Thunder Halls"], command=commmenu)
commmenu.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

devmenu = customtkinter.CTkOptionMenu(app, values=["DevBlogs", "Changelogs"], command=devmenu)
devmenu.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")

settings = customtkinter.CTkButton(app, text="Settings", command=cl_settings)
settings.grid(row=0, column=4, padx=5, pady=10, sticky="nsew")

mirageicon = customtkinter.CTkButton(app, text="Mirage", command=launch_mirage)
mirageicon.grid(row=0, column=5, padx=5, pady=10, sticky="nsew")

# app banner
# Load the image
banner_path = "media/grass.png" 
banner = PILImage.open(banner_path)

# Convert the image into a CTkImage object
ctk_banner = customtkinter.CTkImage(light_image=banner, dark_image=banner, size=(1280, 100))

#########################################3
# Main frame
main_frame = customtkinter.CTkScrollableFrame(app)
main_frame.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Create a label to display the image
banner = customtkinter.CTkLabel(main_frame, image=ctk_banner, text ="")
banner.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

######################################################

# Recommendations frame
recommendations_frame = customtkinter.CTkScrollableFrame(main_frame)
recommendations_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
# welcome the user
labelofuser = f" Recommendations for {username} :"
username_label = customtkinter.CTkLabel(recommendations_frame, text=labelofuser, font=("Roboto", 14), fg_color="transparent")
username_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

##########################################


# All frame
all_frame = customtkinter.CTkScrollableFrame(main_frame)
all_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
# heading for all apps
all_apps = customtkinter.CTkLabel(all_frame, text="All Apps", font=("Roboto", 14), fg_color="transparent")
all_apps.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
# search bar
search_bar = customtkinter.CTkEntry(all_frame, placeholder_text="Search Apps", width=200)
search_bar.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")
def on_search(event=None):
    search_query = search_bar.get()
    # Perform search operation based on the search query
    print(search_query)

search_bar.bind("<Return>", on_search)

##############################################3

# Footer frame
footer_frame = customtkinter.CTkFrame(main_frame)
footer_frame.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

#footer information
footer = customtkinter.CTkLabel(footer_frame, text="Made with ❤️ by @korrykatti", font=("Roboto", 14),text_color="cyan", fg_color="transparent")
footer.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

# more information on the right
more_info = customtkinter.CTkLabel(footer_frame, text="Thunder - Python App Store", font=("Roboto", 18),text_color="cyan", fg_color="transparent")
more_info.grid(row=0, column=1, padx=900, pady=1, sticky="nsew")

# last bit of information
last_infoI = customtkinter.CTkLabel(footer_frame, text="thunderenv.glitch.me", font=("Roboto", 10),text_color="#F7879A", fg_color="transparent")
last_infoI.grid(row=1, column=1, padx=900, pady=1, sticky="nsew")

last_infoII = customtkinter.CTkLabel(footer_frame, text="github.com/korrykatti/Thunder", font=("Roboto", 10),text_color="#F7879A", fg_color="transparent")
last_infoII.grid(row=2, column=1, padx=900, pady=1, sticky="nsew")

logo = PILImage.open("media/icon.png")
logoimage = ImageTk.PhotoImage(logo)
ctk_logo = customtkinter.CTkImage(light_image=logo, dark_image=logo, size=(50, 50))
logolabel = customtkinter.CTkLabel(footer_frame, image=ctk_logo, text ="")
logolabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

last_infoIII = customtkinter.CTkLabel(footer_frame, text="Thank you for using Thunder !", font=("Roboto", 10),text_color="#F7879A", fg_color="transparent")
last_infoIII.grid(row=0, column=0, padx=5, pady=1, sticky="nsew")

#####################################################################################

# Configure grid to be responsive
for i in range(5):
    app.grid_columnconfigure(i, weight=1)

app.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_rowconfigure(3, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

################################################3
if __name__ == '__main__':
    #server_stats()
    app.mainloop()
    



