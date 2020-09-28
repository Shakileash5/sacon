from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import json
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

@app.route("/")
def index():
    global keys,value   
    value = dict(db.child("thesis_data").get().val())
    keys = value.keys()
    return render_template("index.html")

@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "POST":
        data = dict(request.form)
        find = data["name"]
        #print(find)
    try:
        find_key = []   
        for key in keys:
            gets = list(value[key].values())
            find = find.lower()
            for get in gets:
                if isinstance(get, str) :
                    get = get.lower()
                    if find in get:
                        print(find,get)
                        if key not in find_key:
                            find_key.append(key)
                if isinstance(get, list):
                    for l in get:
                        l = l.lower()
                        if find in l:
                            if key not in find_key:
                                find_key.append(key)
                if isinstance(get, int):
                    if find in str(get):
                        if key not in find_key:
                            find_key.append(key)

        print("Matched data's are:::",find_key)
        data = {}
        i = 0
        for key in find_key:
            data[str(i)] = [value[key]["Author"],value[key]["Title"],value[key]["Type"],value[key]["Year"],value[key]["Label"]]
            i = i+1
        data = json.dumps(data)    
        print("Matched data's are:::",data)    
        return data
    except:
            return "500"
                    
    


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)),debug=True,use_reloader=True)