from flask import Flask, render_template
import os
app = Flask(__name__)

################################################################
################# USER DATA HANDLING HERE #######################

#check if local folder exist and create if not
if not os.path.exists('local'):
    os.makedirs('local')




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