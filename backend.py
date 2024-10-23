from flask import Flask,render_template
import os

app = Flask(__name__) 


user_data_file_path = "localdata/userdata.json"


@app.route("/")
def index():
    if os.path.exists(user_data_file_path):
        return("File exists!")
    else:
        return("File does not exist.")

if __name__ == "__main__":  
    app.run(debug=True, port=6969)  
