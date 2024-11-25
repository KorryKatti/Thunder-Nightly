from flask import Flask, render_template, redirect, request
import os
import json
import requests
from bs4 import BeautifulSoup
from flask_caching import Cache

app = Flask(__name__)
app.config['CACHE_TYPE'] = 'SimpleCache'  # Using simple in-memory cache
app.config['CACHE_DEFAULT_TIMEOUT'] = 600  # Cache timeout of 10 minutes
cache = Cache(app)

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

@app.route('/downloadapp', methods=['GET'])
def download_app():
    app_id = request.args.get('app_id')  # Get the app_id from the query parameter
    if app_id:
        print(f"Download requested for app ID: {app_id}")
        return f"Download initiated for app ID: {app_id}"  # For now, return a simple response
    else:
        return "No app ID provided.", 400  # Handle cases where app_id is missing


if __name__ == "__main__":
    app.run(debug=True, port=6969)
