from flask import Flask, render_template, request, jsonify,url_for,redirect
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import pyrebase
from uuid import uuid4

app = Flask(__name__)
CORS(app)


config = {
  "apiKey": "AIzaSyA_DAsVDs2wNv2glJ9hE5KPMNc4tygdDf0",
  "authDomain": "sacon-search.firebaseapp.com",
  "databaseURL": "https://sacon-search.firebaseio.com/",
  "storageBucket": "sacon-search.appspot.com",
  "serviceAccount": "Credentials/sacon-search-firebase-adminsdk-yq4jc-4bc5493504.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
value = dict(db.child("thesis_data").get().val())
keys = value.keys()
storage = firebase.storage()
auth = firebase.auth()

session = {}


@app.route("/")
def index():
    global keys,value,storage   
    value = dict(db.child("thesis_data").get().val())
    keys = value.keys()
    storage = firebase.storage()
    return render_template("index.html")

@app.route("/admin",methods=["GET","POST"])
def admin_login():
    return render_template("admin_login.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = dict(request.form)
        print(data)
        name = data["Uname"]
        password = data["Password"]
        
        try:
            login = dict(auth.sign_in_with_email_and_password(name, password))
            print(login)
            genres = request.json
            token = uuid4()
            session[str(name)] = {"loggedIn":True,"Token":str(token)}
            return jsonify({'redirect': url_for("admin", path=genres,token=token),"token":session[str(name)]["Token"]})
        except:
            #print("fe")
            return "400"

@app.route("/auto_login",methods=["GET","POST"])
def auto_login():
    if request.method == "POST":
        data = dict(request.form)
        keys = session.keys()
        print(session,data)
        for key in keys:
            if session[key]["Token"] == data["Token"] and session[key]["loggedIn"] == True:
                print("Redirect")
                return "redirect"
        return "200"        

@app.route("/upload_form",methods=["GET","POST"])
def upload_form():
    if request.method == "POST":
        data = dict(request.form)
        keys = session.keys()
        print(session,data)
        for key in keys:
            if session[key]["Token"] == data["Token"]:
                return render_template("admin.html",name = key,token = data["Token"])
    return render_template("admin_login.html")        

@app.route("/logout",methods=["GET","POST"])
def logout():
    if request.method == "GET":
        data = dict(request.args)
        print(data)
        keys = session.keys()
        for key in keys:
            if session[key]["Token"] == data["Token"]:
                del session[key]
                print(session)
                return "200"

@app.route("/admin_call",methods=["GET","POST"])
def admin():
    print("val",request.referrer)
    if request.referrer is None:
        return render_template("admin_login.html")
    if "/admin" in request.referrer or "/upload_form" in request.referrer:
        print("allowed!!",request.form,request.args )
        data = dict(request.args)
        name = "Admin"
        keys = session.keys()
        for key in keys:
            if session[key]["Token"] == data["token"]:
                name = key  
        return render_template("admin.html",name = name,token=data["token"])
    else:
        return render_template("admin_login.html")    


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
                        #print(find,get)
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

        #print("Matched data's are:::",find_key)
        data = {}
        i = 0
        for key in find_key:

            data[str(i)] = [value[key]["Author"],value[key]["Title"],value[key]["Thesis type"],value[key]["Year"],value[key]["Label"]]
            i = i+1
        #print(data,type(data),"hh")
        data = json.dumps(data)    
        #print("Matched data value's are:::",data)    
        return data
    except:
            return "500"
                    
@app.route("/get_file",methods = ["GET","POST"])
def get_file():
    if request.method == "POST":
        data = dict(request.form)
        find = data["name"]
        try:
            label = find
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

      data = {"Author": form["Author"], "Year":form["Year"],"University":form["University"],"Title":form["Title"],"Keywords":keywords,"Label":ffile.filename,"Type":form["Type"],
      "Academic department":form["department"],"No of pages":form["pages"]}             
      extention = ffile.filename.split(".")[-1]
      print(data)
      if extention not in ["pdf","docx"]:
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

@app.route("/form")
def form():
    return render_template("form/basic_elements.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)),debug=True,use_reloader=True)