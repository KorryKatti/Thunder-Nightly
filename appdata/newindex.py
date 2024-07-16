import multiprocessing
import webview
import subprocess
import os
import sys
import time
import customtkinter
from PIL import Image as PILImage
from PIL import ImageTk
from PIL import Image
import requests
import json
from funx.fetch_data import fetch_server_stats, ping_server
from bs4 import BeautifulSoup
import time


####################################################3
# checking for apps from the urls
def download_htmls_as_json():
    base_url = "https://korrykatti.github.io/thapps/apps/"
    data_folder = "data"

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)

    while True:
        for app_id in range(1, 100000):
            app_id_str = f"{app_id:05}"
            url = base_url + f"{app_id_str}.html"

            response = requests.get(url)
            if response.status_code == 404:
                print(f"File {app_id_str}.html does not exist. Stopping.")
                return

            soup = BeautifulSoup(response.text, 'html.parser')

            data = {
                "app_id": soup.find('h1', id='appId').text.strip(),
                "app_name": soup.find('h1', id='appName').text.strip(),
                "icon_url": soup.find('h2', id='iconUrl').text.strip(),
                "version": soup.find('h2', id='version').text.strip(),
                "repo_url": soup.find('h2', id='repoUrl').text.strip(),
                "main_file": soup.find('h2', id='mainFile').text.strip(),
                "description": soup.find('h2', id='description').text.strip()
            }

            with open(os.path.join(data_folder, f"{app_id_str}.json"), 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

            print(f"Downloaded data for {app_id_str} as {app_id_str}.json")

        print("Waiting for 2 hours before checking again...")
        time.sleep(2 * 60 * 60)


# Import server stats
stats = fetch_server_stats()
if stats:
    print(f"CPU Usage: {stats['cpu_usage']}%")
    print(f"Memory Usage: {stats['memory_usage']}%")
    print(f"Disk Usage: {stats['disk_usage']}%")

# Ping server
ping_response = ping_server()
if ping_response:
    print("Ping Response:", ping_response)

# Import user data
file_path = 'userdata/userinfo.json'
with open(file_path, 'r') as file:
    data = json.load(file)
username = data['username']
print(f"Username: {username}")



# Basic window which fits 800x640
app = customtkinter.CTk()
app.title("Thunder Client")
app.geometry("1024x640")

def homemenu(choice):
    print(choice)
    if choice == "Home":
        # Recommendations frame
        recommendations_frame = customtkinter.CTkScrollableFrame(main_frame)
        recommendations_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        # Welcome the user
        labelofuser = f" Recommendations for {username} :"
        username_label = customtkinter.CTkLabel(recommendations_frame, text=labelofuser, font=("Roboto", 14), fg_color="transparent")
        username_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # All frame
        all_frame = customtkinter.CTkScrollableFrame(main_frame)
        all_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        # Heading for all apps
        all_apps = customtkinter.CTkLabel(all_frame, text="All Apps", font=("Roboto", 14), fg_color="transparent")
        all_apps.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        # Search bar
        search_bar = customtkinter.CTkEntry(all_frame, placeholder_text="Search Apps", width=200)
        search_bar.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")

        def on_search(event=None):
            search_query = search_bar.get()
            # Perform search operation based on the search query
            print(search_query)

        search_bar.bind("<Return>", on_search)

        # Call app_labels function to populate all_frame with app details
        app_labels(all_frame)

no_image_url_prov = "https://cdn.vectorstock.com/i/500p/65/30/default-image-icon-missing-picture-page-vector-40546530.jpg"

def app_labels(all_frame):
    data_dir = "data"
    filenames = sorted(os.listdir(data_dir), reverse=True)
    for filename in filenames:
        if filename.endswith(".json"):
            try:
                with open(os.path.join(data_dir, filename), "r") as f:
                    app_data = json.load(f)
                    app_id = app_data.get("app_id", "Unknown")
                    app_name = app_data.get("app_data","Unknown")
                    icon_url = app_data.get("icon_url",f"{no_image_url_prov}")
                    version = app_data.get("version","Unknown")
                    repo_url = app_data.get("repo_url","Unknown")
                    main_file = app_data.get("main_file","Unknown")
                    description = app_data.get("description","Unknown")

                    app_labels_for_each = customtkinter.CTkFrame(all_frame)
                    app_labels_for_each.grid(row=1,column=0)

                    test_label = customtkinter.CTkLabel(app_labels,text="Hi how are you")
                    test_label.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
            except Exception as e:
                print(f"Error processing JSON file {filename}: {e}")



def libmenu(choice):
    if choice == "Library":
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()
        print("Library")

        # Configure the main frame grid
        main_frame.grid_columnconfigure(0, weight=1, minsize=200)  # Left frame with a smaller minsize
        main_frame.grid_columnconfigure(1, weight=25)               # Right frame with more space
        main_frame.grid_rowconfigure(0, weight=1)  # Ensure the row stretches to fill the window

        # Library apps name list on the left side
        library_frame = customtkinter.CTkScrollableFrame(main_frame,height=600)
        library_frame.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")
        library_frame.grid_rowconfigure(0, weight=1)  # Ensure library_frame expands vertically

        heading_title_label = customtkinter.CTkLabel(library_frame, text="[ Apps and softwares ]", font=("Roboto", 19), fg_color="transparent")
        heading_title_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")


        # Apps info on the right side
        apps_frame = customtkinter.CTkFrame(main_frame)
        apps_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
        apps_frame.grid_rowconfigure(0, weight=1)  # Ensure apps_frame expands vertically
        apps_frame.grid_columnconfigure(0, weight=1)



    elif choice == "App Update":
        print("App Update")
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()
        # Load app update frame
        app_update_frame = customtkinter.CTkScrollableFrame(main_frame,height=600)
        app_update_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        app_update_frame.grid_rowconfigure(0, weight=1)
        app_update_frame.grid_columnconfigure(0, weight=1)
        app_update_label = customtkinter.CTkLabel(app_update_frame, text="App Update. Check the apps which needs updates here", font=("Roboto", 19), fg_color="transparent")
        app_update_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")



def commmenu(choice):
    print(choice)
    if choice == "Image Board":
        webview.create_window("Image Board", "http://korrykatti.github.io/others/thunder/image.html")
        webview.start()
    elif choice == "Thunder Halls":
        webview.create_window("Thunder Halls", "http://korrykatti.github.io/others/thunder/halls.html")
        webview.start()
    elif choice == "Community":
        webview.create_window("Community", "http://korrykatti.github.io/others/thunder/community.html")
        webview.start()

def devmenu(choice):
    print(choice)
    if choice == "Changelogs":
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # print changelogs from json url
        changelogs_url = "https://korrykatti.github.io/thapps/data/changelog.json"
        response = requests.get(changelogs_url)
        if response.status_code == 200:
            changelogs = response.json()['changelog']  # Access the 'changelog' key
            print(changelogs)

            # show the changelogs in a frame
            changelogs_frame = customtkinter.CTkFrame(main_frame)
            changelogs_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")

            changelogs_label = customtkinter.CTkLabel(changelogs_frame, text="Changelogs", font=("Roboto", 14), fg_color="transparent")
            changelogs_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew", columnspan=2)  # Centering label

            for index, changelog in enumerate(changelogs):
                changelog_label = customtkinter.CTkLabel(changelogs_frame, text=f"{changelog['version']}: {', '.join(changelog['changes'])}", font=("Roboto", 12), fg_color="transparent")
                changelog_label.grid(row=index+1, column=0, padx=5, pady=10, sticky="nsew", columnspan=2)  # Centering label

        elif response.status_code == 404:
            print("Changelogs not found")
        else:
            print("Failed to fetch changelogs")

    elif choice == "DevBlogs":
        webview.create_window("DevBlogs", "https://korrykatti.github.io/thapps/data/index.html")
        webview.start()



def cl_settings():
    print("settings pressed")
    # cd into that directory first and then launch funx/sett_win.py in a different process
    os.chdir("funx")
    subprocess.Popen(["python", "sett_win.py"])
    os.chdir("..")

def launch_mirage():
    print("launching mirage")
    # cd into that directory first and then launch mirage/client.py in a different process
    os.chdir("mirage")
    subprocess.Popen(["python", "client.py"])
    os.chdir("..")

# The option menus on the top
homemenu_option = customtkinter.CTkOptionMenu(app, values=["Home", "Client Update", "Quit"], command=homemenu)
homemenu_option.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

libmenu_option = customtkinter.CTkOptionMenu(app, values=["Library", "App Update"], command=libmenu)
libmenu_option.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")

commmenu_option = customtkinter.CTkOptionMenu(app, values=["Community", "Image Board", "Thunder Halls"], command=commmenu)
commmenu_option.grid(row=0, column=2, padx=5, pady=10, sticky="nsew")

devmenu_option = customtkinter.CTkOptionMenu(app, values=["DevBlogs", "Changelogs"], command=devmenu)
devmenu_option.grid(row=0, column=3, padx=5, pady=10, sticky="nsew")

settings = customtkinter.CTkButton(app, text="Settings", command=cl_settings)
settings.grid(row=0, column=4, padx=5, pady=10, sticky="nsew")

mirageicon = customtkinter.CTkButton(app, text="Mirage", command=launch_mirage)
mirageicon.grid(row=0, column=5, padx=5, pady=10, sticky="nsew")

# App banner
# Load the image
banner_path = "media/grass.png"
banner = PILImage.open(banner_path)

# Convert the image into a CTkImage object
ctk_banner = customtkinter.CTkImage(light_image=banner, dark_image=banner, size=(1280, 100))

# Main frame
main_frame = customtkinter.CTkScrollableFrame(app)
main_frame.grid(row=1, column=0, columnspan=6, padx=5, pady=5, sticky="nsew")

# Create a label to display the image
banner = customtkinter.CTkLabel(main_frame, image=ctk_banner, text="")
banner.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Footer frame
footer_frame = customtkinter.CTkFrame(main_frame)
footer_frame.grid(row=3, column=0, padx=5, pady=10, sticky="nsew")

# Footer information
footer = customtkinter.CTkLabel(footer_frame, text="Made with ❤️ by @korrykatti", font=("Roboto", 14), text_color="cyan", fg_color="transparent")
footer.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")

# More information on the right
more_info = customtkinter.CTkLabel(footer_frame, text="Thunder - Python App Store", font=("Roboto", 18), text_color="cyan", fg_color="transparent")
more_info.grid(row=0, column=1, padx=900, pady=1, sticky="nsew")

# Last bit of information
last_infoI = customtkinter.CTkLabel(footer_frame, text="thunderenv.glitch.me", font=("Roboto", 10), text_color="#F7879A", fg_color="transparent")
last_infoI.grid(row=1, column=1, padx=900, pady=1, sticky="nsew")

last_infoII = customtkinter.CTkLabel(footer_frame, text="github.com/korrykatti/Thunder", font=("Roboto", 10), text_color="#F7879A", fg_color="transparent")
last_infoII.grid(row=2, column=1, padx=900, pady=1, sticky="nsew")

logo = PILImage.open("media/icon.png")
logoimage = ImageTk.PhotoImage(logo)
ctk_logo = customtkinter.CTkImage(light_image=logo, dark_image=logo, size=(50, 50))
logolabel = customtkinter.CTkLabel(footer_frame, image=ctk_logo, text="")
logolabel.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

last_infoIII = customtkinter.CTkLabel(footer_frame, text="Thank you for using Thunder!", font=("Roboto", 10), text_color="#F7879A", fg_color="transparent")
last_infoIII.grid(row=0, column=0, padx=5, pady=1, sticky="nsew")

# Configure grid to be responsive
for i in range(5):
    app.grid_columnconfigure(i, weight=1)

app.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(0, weight=1)
main_frame.grid_rowconfigure(1, weight=1)
main_frame.grid_rowconfigure(2, weight=1)
main_frame.grid_rowconfigure(3, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

# Call homemenu when the app starts
homemenu("Home")
download_htmls_as_json()

if __name__ == '__main__':

    app.mainloop()
