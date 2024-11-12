from flask import Flask, render_template
import os
import json
import requests
import webbrowser
from bs4 import BeautifulSoup

app = Flask(__name__)
USER_DATA_LOADED = False
user_data_file_path = "localdata/userdata.json"
username = None
email = None
profile_picture = None

# Check if the file exists before trying to open it
if os.path.exists(user_data_file_path):
    with open(user_data_file_path) as f:
        data = json.load(f)
        username = data.get("username")
        email = data.get("email")
        profile_picture = data.get("profile_picture")
    USER_DATA_LOADED = True

# Corrected dictionary definition
data_hell_yeah = {
    'username': username,
    'email': email,
    'pfp': profile_picture
}



@app.route("/")
def index():
    if USER_DATA_LOADED:
        return render_template("index.html", **data_hell_yeah)
        
    else:
        return "File does not exist."
    
@app.route("/homepage")
def homepage():
    return render_template("hempej.html",**data_hell_yeah)

@app.route("/store")
def store():
    return render_template("store.html",**data_hell_yeah)

@app.route('/app/<app_id>')
def fetch_app_page(app_id):
    # Construct the URL of the external page
    url = f'https://korrykatti.github.io/thapps/apps/{app_id}.html'
    
    # Fetch the page content
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract elements based on their `id`
        app_data = {
            "app_id": soup.find(id="appId").text if soup.find(id="appId") else "N/A",
            "app_name": soup.find(id="appName").text if soup.find(id="appName") else "N/A",
            "icon_url": soup.find(id="iconUrl").text if soup.find(id="iconUrl") else "",
            "version": soup.find(id="version").text if soup.find(id="version") else "N/A",
            "repo_url": soup.find(id="repoUrl").text if soup.find(id="repoUrl") else "",
            "main_file": soup.find(id="mainFile").text if soup.find(id="mainFile") else "N/A",
            "description": soup.find(id="description").text if soup.find(id="description") else "No description available."
        }
        
        # Render the template with the extracted data
        return render_template('app_page.html', **app_data)
    else:
        # If there is an issue fetching the page, return a 404 error
        return "Page not found", 404
    
    
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:6969")
    app.run(debug=True, port=6969)
