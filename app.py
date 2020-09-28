from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import pyrebase

app = Flask(__name__)

config = {
  "apiKey": "AIzaSyDLYsJm85_J4D0rKZ0TLLMAM-3orCXGE6A",
  "authDomain": "sacon-250805.firebaseapp.com",
  "databaseURL": "https://sacon-250805.firebaseio.com/",
  "storageBucket": "sacon-250805.appspot.com",
  "serviceAccount": "Credentials/sacon-250805-firebase-adminsdk-cc9yo-7d68092103.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
value = dict(db.child("thesis_data").get().val())
keys = value.keys()
print(keys)
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "POST":
        data = dict(request.form)
        find = data["name"]
        print(find)
        
    for key in keys:
        gets = list(value[key].values())
        #print(gets)
        for get in gets:
            if isinstance(get, str) :
                if find in get:
                    print(find)
            if isinstance(get, list):
                for l in get:
                    #print(l)
                    if find in l:
                        print(True)
            if isinstance(get, int):
                if find ==  get:
                    print(find)
    return "200"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)),debug=True,use_reloader=True)