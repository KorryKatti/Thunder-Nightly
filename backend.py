from flask import Flask, render_template
import requests
import json
import os
app = Flask(__name__)

################################################################
################# USER DATA HANDLING HERE #######################

#check if local folder exist and create if not
if not os.path.exists('local'):
    os.makedirs('local')

#check if settings.json exists or not if it does not , create it and add some default values
if not os.path.exists('local/settings.json'):
    with open('local/settings.json', 'w') as f:
        f.write('{\n"server": "http://127.0.0.1:4325"}')
        f.close()


with open('local/settings.json') as f:
    settings = json.load(f)
    server = settings['server']
    f.close()


response = requests.get(server+'/ping')



print("Running on server : ",server)
print('''
Hello welcome to Thunder. Hang on while we ping the server to check if it is up and running
''')
print(response.text)
print("Seems like it worked. Starting app now. Initializing backend")
print("                                     ")
 
#check if server is up and running at server/ping



####################################################################
###################################################################

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    return render_template('logout.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/library')
def library():
    return render_template('library.html')


##################################################################################```
# 
# 
# 
# WE ARE THUNDER UP IN THIS 
#  
# 
# ```##############################################################################



if __name__ == "__main__":
    app.run(debug=True, port=6969)