from flask import Flask, render_template, request, jsonify
from werkzeug import secure_filename
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
storage = firebase.storage()

@app.route("/")
def index():
    global keys,value,storage   
    value = dict(db.child("thesis_data").get().val())
    keys = value.keys()
    storage = firebase.storage()
    return render_template("index.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")


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
                    
@app.route("/get_file",methods = ["GET","POST"])
def get_file():
    if request.method == "POST":
        data = dict(request.form)
        find = data["name"]
        try:
            #label_split = find.split("-")
            #label_split[1] = "0" + label_split[1] + ".pdf"
            #label = ("-").join(label_split)
            #print(label)
            label = find
            if ".pdf" not in find:
                label = find+".pdf"
            myfile = storage.child(label)
            url = myfile.get_url(None)
            print(url)    
            return url
        except:
            return "500"   

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      ffile = request.files['file']
      form = dict(request.form)
      print(form)
      keywords = form["Keywords"]
      keywords = keywords.split(",")
      keys = 0
      i = 0
      for i in range(len(keywords)):
          if "\r" in keywords[i]:
              keywords[i] = keywords[i].replace("\r","")
          if "\n" in keywords[i]:
              keywords[i] = keywords[i].replace("\n","")
          keywords[i] = keywords[i].strip()      
          if len(keywords[i]) == 0:
              keys+=1
      
      for i in range(keys):
        keywords.remove("")   

      data = {"Author": form["Author"], "Year":form["Year"],"University":form["University"],"Title":form["Title"],"Keywords":keywords,"Label":ffile.filename,"Type":form["Type"]}             
      extention = ffile.filename.split(".")[-1]
      print(data)
      if extention != "pdf":
          return '500'
      else:
        ffile.save(secure_filename(ffile.filename))  
        storage.child(ffile.filename).put(ffile.filename)
        os.remove(ffile.filename) 
        val = dict(db.child("thesis_data").get().val())
        print("recieved")
        keys = val.keys() 
        flag = 0
        for key in keys:
            if val[key]["Title"] == data["Title"]:
                print(key)
                db.child("thesis_data").child(key).update(data)
                flag = 1
        if flag == 0:
            db.child("thesis_data").push(data) 
        return render_template("admin.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)),debug=True,use_reloader=True)