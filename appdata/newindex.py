"""TODO:
1. fix mirage
2. fix library
3. fix labels
4. get enough sleep
"""

from bs4 import BeautifulSoup
import markdown
from tkinterhtml import HtmlFrame
import multiprocessing
import webview
import shutil
import zipfile
from tkinter import scrolledtext
import subprocess
import threading
import os
import sys
from tkhtmlview import HTMLLabel
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

# Load the theme from userdata/settings.json
try:
    with open('userdata/settings.json', 'r') as f:
        data = json.load(f)
        theme_name = data.get('theme', 'cyberpunk.json')  # Default theme if 'theme' key is missing
        theme_path = f'themes/{theme_name}'

        # Set the custom tkinter theme
        customtkinter.set_default_color_theme(theme_path)

except FileNotFoundError:
    print("Settings file not found.")
except KeyError:
    print("Theme key 'theme' not found in settings file.")
except Exception as e:
    print(f"Error loading and setting theme: {e}")


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


# Function to download and set up the app
def download_app(app_id):
    # Ensure necessary directories exist
    if not os.path.exists("common/downloading"):
        os.makedirs("common/downloading")
    if not os.path.exists("common/apps"):
        os.makedirs("common/apps")

    # Load app data
    with open(f"data/{app_id}.json", "r") as f:
        app_data = json.load(f)
        repo_url = app_data.get("repo_url")
        app_name = app_data.get("app_name")

    print(f"Downloading {app_name} from {repo_url}...")

    # Download the repository as a zip file
    download_url = f"{repo_url}/archive/refs/heads/main.zip"
    response = requests.get(download_url)
    response.raise_for_status()

    # Save the zip file
    zip_path = f"common/downloading/{app_id}.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    print(f"Repository downloaded successfully as {app_id}.zip")

    # Extract the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall("common/downloading")

    # Find the extracted folder
    extracted_folder = f"common/downloading/{os.path.commonprefix(zip_ref.namelist()).rstrip('/')}"
    new_folder = f"common/apps/{app_id}"

    # Rename and move the folder
    if os.path.exists(new_folder):
        shutil.rmtree(new_folder)
    shutil.move(extracted_folder, new_folder)

    # Remove the zip file
    os.remove(zip_path)

    print(f"Repository extracted and moved to {new_folder}")

    # Update downloads.json
    downloads_file = "userdata/downloads.json"
    if os.path.exists(downloads_file) and os.path.getsize(downloads_file) > 0:
        with open(downloads_file, "r") as f:
            try:
                downloads = json.load(f)
            except json.JSONDecodeError:
                downloads = {}
    else:
        downloads = {}

    downloads[app_id] = {
        "app_name": app_name,
        "repo_url": repo_url
    }

    # Debugging statement to check what is being saved
    print(f"Saving download information: {downloads}")

    with open(downloads_file, "w") as f:
        json.dump(downloads, f, indent=4)

    # Debugging statement to confirm save
    print(f"Download information saved for {app_name}.")

def view_details(app_id):
    global scrolledtext  # Ensure scrolledtext is available in this scope

    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Load app details from JSON file
    json_file_path = f"data/{app_id}.json"
    try:
        with open(json_file_path, "r") as f:
            app_data = json.load(f)
            app_id = app_data.get("app_id", "Unknown")
            app_name = app_data.get("app_name", "Unknown")
            icon_url = app_data.get("icon_url", no_image_url_prov)
            version = app_data.get("version", "Unknown")
            repo_url = app_data.get("repo_url", "Unknown")
            main_file = app_data.get("main_file", "Unknown")
            description = app_data.get("description", "Unknown")

            # Display app details
            app_name_label = customtkinter.CTkLabel(main_frame, text=f"App Name: {app_name}", font=("Roboto", 14), fg_color="transparent")
            app_name_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

            version_label = customtkinter.CTkLabel(main_frame, text=f"Version: {version}", font=("Roboto", 14), fg_color="transparent")
            version_label.grid(row=2, column=1, padx=5, pady=10, sticky="e")

            description_label = customtkinter.CTkLabel(main_frame, text=f"Description: {description}", font=("Roboto", 14), fg_color="transparent")
            description_label.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky="w")

            repo_label = customtkinter.CTkLabel(main_frame, text=f"You are downloading this app from: {repo_url}. We do not scan the apps for malicious code; you can report if you find any app with such.", font=("Roboto", 14), fg_color="transparent")
            repo_label.grid(row=3, column=0, padx=5, pady=10, sticky="w")

            # Display app icon
            try:
                response = requests.get(icon_url, stream=True)
                if response.status_code == 200:
                    image = Image.open(response.raw)
                else:
                    image = Image.open(no_image_url_prov)
            except Exception:
                image = Image.open(no_image_url_prov)

            image = image.resize((100, 100))
            photo = ImageTk.PhotoImage(image)
            icon_label = customtkinter.CTkLabel(main_frame, image=photo, text="")
            icon_label.image = photo
            icon_label.grid(row=1, column=1, padx=5, pady=10, sticky="e")

            main_file_label = customtkinter.CTkLabel(main_frame, text=f"This app runs from: {main_file}", font=("Roboto", 14), fg_color="transparent")
            main_file_label.grid(row=4, column=0, padx=5, pady=10, sticky="w")

            # Back button
            back_button = customtkinter.CTkButton(main_frame, text="Back", command=lambda: back_to_home())
            back_button.grid(row=5, column=0, padx=5, pady=10, sticky="e")

            # Create a placeholder for the README.md content ( chatgpt wrote this )
            readme_frame = customtkinter.CTkFrame(main_frame, height=200)
            readme_frame.grid(row=6, column=0, columnspan=2, padx=5, pady=10, sticky="nsew")
            readme_label = scrolledtext.ScrolledText(readme_frame, wrap="word", width=80, height=10)
            readme_label.pack(fill="both", expand=True)

            # Loading message while fetching README
            loading_label = customtkinter.CTkLabel(readme_frame, text="Loading README...If this fails then probably the author hasn't put a file for it", font=("Roboto", 14), fg_color="transparent")
            loading_label.pack(fill="both", expand=True)

            # download button
            download_button = customtkinter.CTkButton(main_frame, text="Download", command=lambda: download_app(app_id))
            download_button.grid(row=7, column=0, padx=5, pady=10, sticky="e")

            # comment section
            comment_label = customtkinter.CTkLabel(main_frame,text="Comments",font=("Calibri",16),fg_color="transparent")
            comment_label.grid(row=8,column=0,padx=5,pady=10,sticky="w")
            comments_frame = customtkinter.CTkScrollableFrame(main_frame)
            comments_frame.grid(row=9,column=0,columnspan=2,padx=5,pady=10,sticky="ew")
            comingsoon = customtkinter.CTkLabel(comments_frame,text="Coming soon.............")
            comingsoon.grid(row=0,column=0,padx=5,pady=10,sticky="w")
            # Load the README.md content asynchronously
            def load_readme():
                readme_url = f"{repo_url}/raw/main/thunder.md"
                try:
                    readme_response = requests.get(readme_url)
                    if readme_response.status_code == 200:
                        readme_md = readme_response.text
                        readme_html = markdown.markdown(readme_md)
                        # Clear loading message and display README content
                        loading_label.pack_forget()
                        readme_label.delete(1.0, "end")  # Clear previous content
                        readme_label.insert("end", readme_html)  # Insert new HTML content
                    else:
                        raise Exception("Failed to load README.md")
                except Exception as e:
                    loading_label.configure(text=f"Error loading README.md: {e}")

            threading.Thread(target=load_readme).start()

    except FileNotFoundError:
        print(f"Error: JSON file {json_file_path} not found.")
    except Exception as e:
        print(f"Error loading app details for {app_id}: {e}")

def back_to_home():
    # Clear the main frame
    for widget in main_frame.winfo_children():
        widget.destroy()


    # Call the home menu function
    homemenu("Home")

# Basic window which fits 800x640
app = customtkinter.CTk()
app.title("Thunder Client")
app.geometry("1024x640")

def homemenu(choice):
    print(choice)
    if choice == "Home":
        for widget in main_frame.winfo_children():
            widget.destroy()
        # Recommendations frame
        recommendations_frame = customtkinter.CTkScrollableFrame(main_frame)
        recommendations_frame.grid(row=1, column=0, padx=5, pady=10, sticky="nsew")
        recommend_labels(recommendations_frame)
        # Welcome the user
        labelofuser = f" Recommendations for {username} :"
        username_label = customtkinter.CTkLabel(recommendations_frame, text=labelofuser, font=("Roboto", 14), fg_color="transparent")
        username_label.grid(row=0, column=0, padx=5, pady=10, sticky="nsew")

        # All frame
        all_frame = customtkinter.CTkScrollableFrame(main_frame,width=700)
        all_frame.grid(row=2, column=0, padx=5, pady=10, sticky="nsew")
        # Heading for all apps
        all_apps = customtkinter.CTkLabel(all_frame, text=" [ All Apps ]", font=("Roboto", 20), fg_color="transparent")
        all_apps.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        # Search bar
        search_bar = customtkinter.CTkEntry(all_frame, placeholder_text="Search Apps", width=200)
        search_bar.grid(row=0, column=25, padx=5, pady=10, sticky="e")

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


        def on_search(event=None):
            search_query = search_bar.get()
            # Perform search operation based on the search query
            print(search_query)

        search_bar.bind("<Return>", on_search)

        # Call app_labels function to populate all_frame with app details
        app_labels(all_frame)

no_image_url_prov = "https://cdn.vectorstock.com/i/500p/65/30/default-image-icon-missing-picture-page-vector-40546530.jpg"

def search_results(search_query):
    # Perform search operation based on the search query
    print(search_query)

def app_labels(all_frame):
    data_dir = "data"
    filenames = sorted(os.listdir(data_dir), reverse=True)

    # Counter for grid row
    row_counter = 1

    for filename in filenames:
        if filename.endswith(".json"):
            try:
                with open(os.path.join(data_dir, filename), "r") as f:
                    app_data = json.load(f)
                    app_id = app_data.get("app_id", "Unknown")
                    app_name = app_data.get("app_name", "Unknown")
                    icon_url = app_data.get("icon_url", f"{no_image_url_prov}")
                    version = app_data.get("version", "Unknown")
                    repo_url = app_data.get("repo_url", "Unknown")
                    main_file = app_data.get("main_file", "Unknown")
                    description = app_data.get("description", "Unknown")

                    app_labels_for_each = customtkinter.CTkFrame(all_frame,width=700)
                    app_labels_for_each.grid(row=row_counter, column=0)

                    # Separator line above app details
                    separator_above = customtkinter.CTkLabel(app_labels_for_each, text="-")
                    separator_above.grid(row=1, column=11, columnspan=4, padx=5, pady=10, sticky="n")

                    # Display app name
                    app_name_label = customtkinter.CTkLabel(app_labels_for_each, text=f"App Name: {app_name}", font=("Roboto", 14), fg_color="transparent")
                    app_name_label.grid(row=2, column=0, padx=5, pady=10,sticky="w")

                    # Display version
                    version_label = customtkinter.CTkLabel(app_labels_for_each, text=f"Version: {version}", font=("Roboto", 14), fg_color="transparent")
                    version_label.grid(row=2, column=10, padx=5, pady=10,sticky="e")

                    # Display description
                    description_label = customtkinter.CTkLabel(app_labels_for_each, text=f"Description: {description}", font=("Roboto", 14), fg_color="transparent")
                    description_label.grid(row=3, column=0, columnspan=2, padx=5, pady=10,sticky="w")

                    # download button
                    download_button = customtkinter.CTkButton(app_labels_for_each, text="View Details", command=lambda app_id=app_id: view_details(app_id))

                    download_button.grid(row=3, column=10, padx=5, pady=10, sticky="e")

                    # Separator line below app details
                    separator_below = customtkinter.CTkLabel(app_labels_for_each, text="-")
                    separator_below.grid(row=4, column=11, columnspan=2, padx=5, pady=10, sticky="s")

                    # Increment row counter for next app
                    row_counter += 5  # Adjusted for the 4 rows used (including separators)

            except Exception as e:
                print(f"Error processing JSON file {filename}: {e}")


def recommend_labels(recommendations_frame):
    # Open and read the JSON file
    with open("aegis/base.json", "r") as f:
        data = json.load(f)

    # Print the IDs
    for app_id in data:
        print(app_id)
    data_dir = "data"
    filenames = sorted(os.listdir(data_dir), reverse=True)

    # Counter for grid row and column
    row_counter = 1
    column_counter = 1
    max_columns = 5

    for filename in filenames:
        if filename.endswith(".json"):
            try:
                with open(os.path.join(data_dir, filename), "r") as f:
                    app_data = json.load(f)
                    app_id = app_data.get("app_id", "Unknown")
                    app_name = app_data.get("app_name", "Unknown")
                    version = app_data.get("version", "Unknown")

                    if app_id in data:
                        recomm_labels_for_each = customtkinter.CTkFrame(recommendations_frame, width=200, height=200)
                        recomm_labels_for_each.grid(row=row_counter, column=column_counter, padx=10, pady=10)

                        app_name_label = customtkinter.CTkLabel(recomm_labels_for_each, text=f"{app_name}", font=("Roboto", 14), fg_color="transparent")
                        app_name_label.grid(row=0, column=0, padx=5, pady=5)

                        version_label = customtkinter.CTkLabel(recomm_labels_for_each, text=f"Version: {version}", font=("Roboto", 12), fg_color="transparent")
                        version_label.grid(row=1, column=0, padx=5, pady=5)

                        view_button = customtkinter.CTkButton(recomm_labels_for_each, text="View", command=lambda app_id=app_id: view_details(app_id))
                        view_button.grid(row=2, column=0, padx=5, pady=5)

                        separator1 = customtkinter.CTkLabel(recomm_labels_for_each, text="|")
                        separator1.grid(row=0, column=1, padx=5, pady=5)

                        separator2 = customtkinter.CTkLabel(recomm_labels_for_each, text="|")
                        separator2.grid(row=1, column=1, padx=5, pady=5)

                        separator3 = customtkinter.CTkLabel(recomm_labels_for_each, text="|")
                        separator3.grid(row=2, column=1, padx=5, pady=5)

                        column_counter += 1
                        if column_counter >= max_columns:
                            column_counter = 1
                            row_counter += 1
            except Exception as e:
                print(f"Error processing JSON file {filename}: {e}")


def view_lib_details(app_id):
    print(app_id)
    with open(f"data/{app_id}.json", "r") as f:
        app_data = json.load(f)
        app_id = app_data.get("app_id", "Unknown")
        app_name = app_data.get("app_name", "Unknown")
        app_description = app_data.get("description", "Unknown")
        app_version = app_data.get("version", "Unknown")
        app_repo_url = app_data.get("repo_url", "Unknown")
        app_main_file = app_data.get("main_file", "Unknown")
        icon_url = app_data.get("icon_url", f"{no_image_url_prov}")
 # Apps info on the right side
    apps_frame = customtkinter.CTkFrame(main_frame)
    apps_frame.grid(row=0, column=1, padx=5, pady=10, sticky="nsew")
    apps_frame.grid_columnconfigure(0, weight=1)
    apps_frame.grid_columnconfigure(1, weight=10)
    apps_frame.grid_columnconfigure(2, weight=10)
    apps_frame.grid_columnconfigure(3, weight=10)
    apps_frame.grid_rowconfigure(0, weight=1)
    apps_frame.grid_rowconfigure(1, weight=77)
    apps_frame.grid_rowconfigure(2, weight=99)
    apps_frame.grid_rowconfigure(3, weight=1)



    # Display app details
    app_id_label = customtkinter.CTkLabel(apps_frame, text=f"App ID: {app_id}", font=("Roboto", 14), fg_color="transparent")
    app_id_label.grid(row=0, column=0, padx=5, pady=10, sticky="nw")

    app_name_label = customtkinter.CTkLabel(apps_frame, text=f"App Name: {app_name}", font=("Roboto", 14), fg_color="transparent")
    app_name_label.grid(row=0, column=3, padx=5, pady=10, sticky="ne")

           # Display app icon
    try:
        response = requests.get(icon_url, stream=True)
        if response.status_code == 200:
            image = Image.open(response.raw)
        else:
            image = Image.open(no_image_url_prov)
    except Exception:
        image = Image.open(no_image_url_prov)

    image = image.resize((100, 100))
    photo = ImageTk.PhotoImage(image)
    icon_label = customtkinter.CTkLabel(apps_frame, image=photo, text="")
    icon_label.image = photo
    icon_label.grid(row=1, column=0, padx=5, pady=10, sticky="nw")

    # Display app description
    description_label = customtkinter.CTkLabel(apps_frame, text=f"Description: {app_description}", font=("Roboto", 14), fg_color="transparent")
    description_label.grid(row=1, column=3, padx=5, pady=10, sticky="ne")

    # Display app version
    version_label = customtkinter.CTkLabel(apps_frame, text=f"Version: {app_version}", font=("Roboto", 14), fg_color="transparent")
    version_label.grid(row=1, column=2, padx=5, pady=10, sticky="nw")

    # start app button
    start_button = customtkinter.CTkButton(apps_frame, text="Start", command=lambda app_id=app_id: start_app(app_id))
    start_button.grid(row=2, column=2, padx=1, pady=10, sticky="ne")

    # uninstall app button
    uninstall_button = customtkinter.CTkButton(apps_frame, text="Uninstall", command=lambda app_id=app_id: uninstall_app(app_id))
    uninstall_button.grid(row=2, column=1, padx=1, pady=10, sticky="ne")

    # open repo button
    open_repo_button = customtkinter.CTkButton(apps_frame, text="Open Repo", command=lambda app_id=app_id: open_repo(app_id))
    open_repo_button.grid(row=2, column=0, padx=1, pady=10, sticky="ne")


    # textbox with aegis data (coming soon)
    aegis_label = customtkinter.CTkLabel(apps_frame, text="AEGIS Data", font=("Roboto", 14), fg_color="transparent")
    aegis_label.grid(row=3, column=0, padx=5, pady=10, sticky="ew")
    aegis_textbox = customtkinter.CTkTextbox(apps_frame ,width=300, height=200)
    aegis_textbox.grid(row=4, column=0, padx=5, pady=10, sticky="ew")
    aegis_textbox.insert("0.0", "Coming soon")
    aegis_textbox.configure(state="disabled")

def latest_version(app_id):
    url = f"https://korrykatti.github.io/thapps/apps/{app_id}.html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        version_tag = soup.find('h2', id='version')
        if version_tag:
            latest_ver = version_tag.text.strip()
            return latest_ver
        else:
            print(f"Version tag not found for app_id: {app_id}")
            return None
    else:
        print(f"Failed to fetch URL: {url}, status code: {response.status_code}")
        return None




def view_up_details(app_id):
    # make a frame on left displaying the app name and version along with app id
    with open (f"data/{app_id}.json", "r") as f:
        app_data = json.load(f)
        app_id = app_data.get("app_id", "Unknown")
        app_name = app_data.get("app_name", "Unknown")
        app_description = app_data.get("description", "Unknown")
        app_version = app_data.get("version", "Unknown")
        app_repo_url = app_data.get("repo_url", "Unknown")
        app_main_file = app_data.get("main_file", "Unknown")
        icon_url = app_data.get("icon_url", f"{no_image_url_prov}")

    view_updates_frame = customtkinter.CTkFrame(main_frame)
    view_updates_frame.grid(row=0, column=1, padx=5, pady=10, sticky="e")
    view_updates_frame.grid_columnconfigure(1, weight=100)
    view_updates_frame.grid_rowconfigure(1,weight=1)
    test_label = customtkinter.CTkLabel(view_updates_frame, text=f"App ID: {app_id}", font=("Roboto", 14), fg_color="transparent")
    test_label.grid(row=0, column=0, padx=5, pady=10, sticky="w")
    version_label = customtkinter.CTkLabel(view_updates_frame, text=f"Version : {app_version}", font=("Roboto", 14), fg_color="transparent")
    version_label.grid(row=1, column=0, padx=5, pady=10, sticky="w")

    latest_ver = latest_version(app_id)
    if latest_ver != app_version:
        update_label = customtkinter.CTkLabel(view_updates_frame, text=f"Update Available: {latest_version}", font=("Roboto", 14), fg_color="transparent")
        update_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")
    else:
        update_label = customtkinter.CTkLabel(view_updates_frame, text=f"No Update Available", font=("Roboto", 14), fg_color="transparent")
        update_label.grid(row=2, column=0, padx=5, pady=10, sticky="w")




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

        # display app name of app id which exist in userdata/downloads.json
        with open("userdata/downloads.json", "r") as f:
            data = json.load(f)
            row_counter = 1
            for app_id in data:
                app_name = data[app_id]["app_name"]
                app_name_button = customtkinter.CTkButton(library_frame, text=app_name, command=lambda app_id=app_id: view_lib_details(app_id))
                app_name_button.grid(row=row_counter, column=0, padx=5, pady=10, sticky="nsew")
                row_counter += 1

    elif choice == "App Update":
        print("App Update")
        # Clear main frame
        for widget in main_frame.winfo_children():
            widget.destroy()

        # add a list of downloaded apps at left in a new frame
        app_update_frame = customtkinter.CTkScrollableFrame(main_frame,width=300)
        app_update_frame.grid(row=0, column=0, padx=5, pady=10, sticky="w")
        app_update_frame.grid_rowconfigure(0, weight=99)  # Ensure library_frame expands vertically
        # display app name of app id which exist in userdata/downloads.json as a button
        with open("userdata/downloads.json", "r") as f:
            data = json.load(f)
            row_counter = 1
            for app_id in data:
                app_name = data[app_id]["app_name"]
                app_name_button = customtkinter.CTkButton(app_update_frame, text=app_name, command=lambda app_id=app_id: view_up_details(app_id))
                app_name_button.grid(row=row_counter, column=0, padx=5, pady=10, sticky="nsew")
                row_counter += 1


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
