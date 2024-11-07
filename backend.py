from flask import Flask, render_template
import os
import json

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

if __name__ == "__main__":
    app.run(debug=True, port=6969)
