from flask import Flask, render_template, redirect, request
import os
import json
import requests
from bs4 import BeautifulSoup
from flask_caching import Cache
from urllib.parse import urlparse
import threading

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'  # Using simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 600  # Cache timeout of 10 minutes
cache = Cache(app)
index_file = "applications/index.json"
if not os.path.exists(index_file):
    with open(index_file, 'w') as f:
        json.dump({"downloaded_apps": []}, f)

USER_DATA_LOADED = False
user_data_file_path = "localdata/userdata.json"
username = None
email = None
profile_picture = None

# Load user data if the file exists
if os.path.exists(user_data_file_path):
    with open(user_data_file_path) as f:
        data = json.load(f)
        username = data.get("username")
        email = data.get("email")
        profile_picture = data.get("profile_picture")
    USER_DATA_LOADED = True

# User data dictionary
data_hell_yeah = {
    'username': username,
    'email': email,
    'pfp': profile_picture
}

# Function to scrape app data
def scrape_app_data(app_id):
    url = f'https://korrykatti.github.io/thapps/apps/{app_id:05}.html'
    response = requests.get(url)
    if response.status_code == 404:
        return None  # Stop fetching if page doesn't exist
    elif response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return {
            "app_id": f"{app_id:05}",
            "app_name": soup.find(id="appName").text if soup.find(id="appName") else "N/A",
            "icon_url": soup.find(id="iconUrl").text if soup.find(id="iconUrl") else "",
            "version": soup.find(id="version").text if soup.find(id="version") else "N/A",
            "repo_url": soup.find(id="repoUrl").text if soup.find(id="repoUrl") else "",
            "main_file": soup.find(id="mainFile").text if soup.find(id="mainFile") else "N/A",
            "description": soup.find(id="description").text if soup.find(id="description") else "No description available."
        }
    return None

# Route for the all apps page
@app.route("/allapps")
def allappslist():
    # Check if cached data exists
    all_apps_data = cache.get('all_apps_data')
    if not all_apps_data:
        all_apps_data = []
        app_id = 1
        while True:
            app_data = scrape_app_data(app_id)
            if app_data is None:
                break
            all_apps_data.append(app_data)
            app_id += 1
        cache.set('all_apps_data', all_apps_data)  # Cache the data
    return render_template("allappslist.html", apps=all_apps_data, **data_hell_yeah)

# Route to refresh the cache
@app.route("/refresh-cache", methods=["POST"])
def refresh_cache():
    cache.clear()  # Clear all cached data
    return redirect("/allapps")  # Redirect to the all apps page

# Main route and other pages
@app.route("/")
def index():
    if USER_DATA_LOADED:
        return render_template("index.html", **data_hell_yeah)
    else:
        return "File does not exist."

@app.route("/homepage")
def homepage():
    return render_template("hempej.html", **data_hell_yeah)

@app.route("/store")
def store():
    return render_template("store.html", **data_hell_yeah)

@app.route('/app/<app_id>')
def fetch_app_page(app_id):
    url = f'https://korrykatti.github.io/thapps/apps/{app_id}.html'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        app_data = {
            "app_id": soup.find(id="appId").text if soup.find(id="appId") else "N/A",
            "app_name": soup.find(id="appName").text if soup.find(id="appName") else "N/A",
            "icon_url": soup.find(id="iconUrl").text if soup.find(id="iconUrl") else "",
            "version": soup.find(id="version").text if soup.find(id="version") else "N/A",
            "repo_url": soup.find(id="repoUrl").text if soup.find(id="repoUrl") else "",
            "main_file": soup.find(id="mainFile").text if soup.find(id="mainFile") else "N/A",
            "description": soup.find(id="description").text if soup.find(id="description") else "No description available."
        }
        return render_template('app_page.html', **app_data)
    else:
        return "Page not found", 404
    

if not os.path.exists('applications'):
    os.makedirs('applications')
    print("Folder 'applications' created.")
else:
    print("Folder 'applications' already exists.")

if not os.path.exists('temp'):
    os.makedirs('temp')
    print("Folder 'temp' created.")
else:
    print("Folder 'temp' already exists.")

import shutil


def allcheckpass_run(app_data):
    pass

def run_app_thread(app_id):
    app_data = scrape_app_data(int(app_id))
    if app_data:
        app_name = app_data["app_name"]
        repo_url = app_data["repo_url"]
        main_file = app_data["main_file"]
        print(f"Running app: {app_name} from repository: {repo_url}")

    app_dir = f'applications/{app_id}'

    # Check for existing folders inside `applications/<app_id>`
    if os.path.exists(app_dir):
        subdirs = [d for d in os.listdir(app_dir) if os.path.isdir(os.path.join(app_dir, d))]
        if subdirs:
            old_folder_path = os.path.join(app_dir, subdirs[0])
            if old_folder_path != app_dir:
                # Merge contents of old folder into target folder
                for item in os.listdir(old_folder_path):
                    src_path = os.path.join(old_folder_path, item)
                    dest_path = os.path.join(app_dir, item)
                    if os.path.exists(dest_path):
                        print(f"Skipping existing item: {dest_path}")
                    else:
                        shutil.move(src_path, dest_path)

                # Delete the old folder after merging
                os.rmdir(old_folder_path)
                print(f"Renamed and merged folder {old_folder_path} into {app_dir}")
        else:
            print(f"No folders found inside {app_dir}")
    else:
        os.makedirs(app_dir)
        print(f"Created directory: {app_dir}")

    print(f"App {app_id} setup completed.")
    return "success"

    allcheckpass_run(app_data)




import zipfile

@app.route('/run/<app_id>')
def run_app(app_id):
    zip_path = f'applications/{app_id}/master.zip'
    app_dir = f'applications/{app_id}'

    # Handle zip extraction if the zip file exists
    if os.path.exists(zip_path):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(app_dir)
        os.remove(zip_path)
        print(f"Extraction successful for {zip_path}.")
    else:
        print(f"Zip file not found at {zip_path}.")

    print("Initial setup check passed.")

    # Run the app in a separate thread
    thread = threading.Thread(target=run_app_thread, args=(app_id,))
    thread.start()

    return f"App {app_id} is being processed. Check logs for progress."



def downloadapp(app_id):
    # Scrape the app data to get the repository URL
    app_data = scrape_app_data(int(app_id))
    if app_data and app_data.get("repo_url"):
        repo_url = app_data["repo_url"]
        print(f"Repository URL for app ID {app_id}: {repo_url}")
        
        # GitHub repository branches to check
        branches_to_check = ["main", "master", "thunder"]
        
        # Create a folder named after the app_id under the 'applications' directory
        temp_folder = f'applications/{app_id}'
        if not os.path.exists(temp_folder):
            os.makedirs(temp_folder)
            print(f"Folder '{temp_folder}' created.")
        
        # Check if the index.json file exists
        index_file_path = 'applications/index.json'
        if not os.path.exists(index_file_path):
            # Create the index.json file if it doesn't exist
            with open(index_file_path, 'w') as index_file:
                json.dump({"downloaded_apps": []}, index_file)
                print("Index file created.")
        
        # Load the index.json to check existing downloaded apps
        with open(index_file_path, 'r') as index_file:
            index_data = json.load(index_file)
            downloaded_apps = index_data["downloaded_apps"]
        
        # Check if the app_id is already in the list
        if app_id in downloaded_apps:
            return f"App ID {app_id} has already been downloaded."

        # Check each branch and try to get the .zip file
        for branch in branches_to_check:
            # Construct the URL for the branch's ZIP download
            branch_url = f"{repo_url.rstrip('/')}/archive/refs/heads/{branch}.zip"
            response = requests.get(branch_url)
            
            # If the branch exists (status code 200), download the ZIP
            if response.status_code == 200:
                print(f"Branch '{branch}' found. Downloading the ZIP...")
                # Extract the filename from the URL
                file_name = f"{branch}.zip"
                file_path = os.path.join(temp_folder, file_name)

                # Save the ZIP file to the folder
                with open(file_path, 'wb') as file:
                    file.write(response.content)
                print(f"Repository downloaded and saved to {file_path}.")
                
                # Update the index.json file with the downloaded app_id
                downloaded_apps.append(app_id)
                index_data["downloaded_apps"] = downloaded_apps
                with open(index_file_path, 'w') as index_file:
                    json.dump(index_data, index_file)
                print(f"App ID {app_id} added to index.")
                
                return f"Download initiated for app ID: {app_id}. Repository saved to {file_path}."
        
        # If no branches were found
        return f"None of the branches ({', '.join(branches_to_check)}) exist for the repository {repo_url}."
    
    else:
        return f"App ID {app_id} not found or repository URL is missing."


@app.route('/downloadapp', methods=['GET'])
def download_app():
    app_id = request.args.get('app_id')  # Get the app_id from the query parameter
    if app_id:
        return downloadapp(app_id)  # Call the function and return its response
    else:
        return "App ID is missing", 400  # Handle cases where app_id is missing


@app.route('/library', methods=['GET'])
def library():
    # Load JSON data
    json_file = os.path.join("applications", "index.json")  # Adjust the path if needed
    with open(json_file, "r") as file:
        app_data = json.load(file)

    # Extract downloaded app IDs or provide a default empty list
    downloaded_apps = app_data.get("downloaded_apps", [])

    # Pass data to the template
    return render_template("library.html", downloaded_apps=downloaded_apps)


@app.errorhandler(404)
def not_found(error):
    # Render the custom 404 template
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(debug=True, port=6969)
