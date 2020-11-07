from flask import Flask, render_template, request, jsonify,url_for,redirect
from werkzeug.utils import secure_filename
from flask_cors import CORS
import os
import json
import pyrebase
from uuid import uuid4
import sys

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

def load_data():
    global keys,value,storage   
    value = dict(db.child("thesis_data").get().val())
    keys = value.keys()
    storage = firebase.storage()

@app.route("/")
def index():
    load_data()
    return render_template("index.html")

@app.route("/admin",methods=["GET","POST"])
def admin_login():
    return render_template("admin_login.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        data = dict(request.form)
        name = data["Uname"]
        password = data["Password"]
        
        try:
            login = dict(auth.sign_in_with_email_and_password(name, password))
            genres = request.json
            token = uuid4()
            session[str(name)] = {"loggedIn":True,"Token":str(token)}
            return jsonify({'redirect': url_for("admin", path=genres,token=token),"token":session[str(name)]["Token"]})
            #return jsonify({'redirect': url_for("form", path=genres,token=token),"token":session[str(name)]["Token"]})
        except:
            #print("fe")
            return "400"
    return redirect(url_for("admin_login"))         

@app.route("/auto_login",methods=["GET","POST"])
def auto_login():
    if request.method == "POST":
        data = dict(request.form)
        keys = session.keys()
        #print(session,data)
        for key in keys:
            if session[key]["Token"] == data["Token"] and session[key]["loggedIn"] == True:
                return "redirect"
        return "200"        
    return redirect(url_for("admin_login")) 

@app.route("/upload_form",methods=["GET","POST"])
def upload_form():
    if request.method == "POST":
        data = dict(request.form)
        keys = session.keys()
        #print(session,data,"upload_form")
        for key in keys:
            if session[key]["Token"] == data["Token"]:
                #return render_template("admin.html",name = key,token = data["Token"])
                return render_template("form/basic_elements.html",name = key,token = data["Token"])
    return redirect(url_for("admin_login"))        

@app.route("/logout",methods=["GET","POST"])
def logout():
    if request.method == "GET":
        data = dict(request.args)
        keys = session.keys()
        for key in keys:
            if session[key]["Token"] == data["Token"]:
                del session[key]
                return "200"
    return redirect(url_for("admin_login")) 

@app.route("/admin_call",methods=["GET","POST"])
def admin():
    #print("val",request.referrer)
    if request.referrer is None:
        return render_template("admin_login.html")
    if "/admin" in request.referrer or "/upload_form" in request.referrer:
        data = dict(request.args)
        name = "Admin"
        keys = session.keys()
        for key in keys:
            if session[key]["Token"] == data["token"]:
                name = key         
        #return render_template("admin.html",name = name,token=data["token"])
        return render_template("form/basic_elements.html",name = name,token=data["token"])
    else:
        return redirect(url_for("admin_login"))    


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
        #print("debug:::")
        for key in find_key:
            data[str(i)] = [value[key]["Author"],value[key]["Year"],value[key]["Title"],value[key]["Academic department"],value[key]["City"],value[key]["University"],value[key]["No of pages"],value[key]["Thesis type"],value[key]["Label"],value[key]['Keywords'],key]
            i = i+1
            
        #print(data,type(data),"hh")
        data = json.dumps(data)    
        #print("Matched data value's are:::",data)    
        return data
    except:
            #print(sys.exc_info()[0])
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
            return url
        except:
            return "500"   
    return redirect(url_for("index"))

@app.route("/get_thesis", methods = ["GET","POST"])
def get_thesis():
    if request.method == "GET":
        try:
            key = dict(request.args)["key"]
            #print("The key ::",key)
            data = [value[key]["Author"],value[key]["Year"],value[key]["Title"],value[key]["Academic department"],value[key]["City"],value[key]["University"],value[key]["No of pages"],value[key]["Thesis type"],value[key]["Label"],value[key]['Keywords'],key]
            data = json.dumps(data) 
            return data
        except:    
            return "500"
    return redirect(url_for("admin_login"))

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      ffile = request.files['file']
      form = dict(request.form)
      token = form["token"]
      keywords = form["Keywords"]
      if len(keywords)==0:
          keywords = ["Null"]
      else:    
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
      i = 0
      for key in form.keys():
          if len(form[key]) == 0:
              form[key] = "__"

      data = {"Author": form["Author"], "Year":form["Year"],"City":form["City"],"University":form["University"],"Title":form["Title"],"Keywords":keywords,"Label":ffile.filename,"Thesis type":form["Type"],
      "Academic department":form["department"],"No of pages":form["pages"]}             
      extention = ffile.filename.split(".")[-1]
      
      if extention not in ["pdf","docx"]:
          return render_template("form/basic_elements.html",token=token,upload="2")
      else:
        try:
            ffile.save(secure_filename(ffile.filename))  
            filename = ffile.filename.split('.')
            filename[0] = filename[0].replace(" ","_")
            filename = '.'.join(filename)
            data["Label"] = filename           
            print("::::file_uploading::::")
            storage.child(filename).put(filename)
            print("::::file_uploaded::::")
            os.remove(filename) 
            val = dict(db.child("thesis_data").get().val())
            #print("recieved")
            keys = val.keys() 
            flag = 0
            for key in keys:
                if val[key]["Title"] == data["Title"]:
                    db.child("thesis_data").child(key).update(data)
                    flag = 1
            if flag == 0:
                db.child("thesis_data").push(data) 
            load_data()    
            return render_template("form/basic_elements.html",token=token,upload="1")
        except:
            return render_template("form/basic_elements.html",token=token,upload="3")   
   return redirect(url_for("admin_login"))        

@app.route("/update",methods=["GET","POST"])
def update():
    if request.method == "POST":
        data = dict(request.form)
        token = data["token"]
        del data["token"]
        keywords = data["Keywords"]
        ffile = request.files['file']
        if len(keywords)==0:
          keywords = ["Null"]
        else:    
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
        data["Keywords"] = keywords       
        if len(ffile.filename) == 0:
            print("Empty")
        else:
            
            extention = ffile.filename.split(".")[-1]  
            if extention not in ["pdf","docx"]:
                return render_template("form/basic_elements.html",token=token,update="2") 
            else:
                ffile.save(secure_filename(ffile.filename))  
                filename = ffile.filename.split('.')
                filename[0] = filename[0].replace(" ","_")
                filename = '.'.join(filename) 
                storage.delete(data["Label"])
                data["Label"] = filename
                storage.child(filename).put(filename)
                os.remove(filename) 
        try:            
            key = data["keyv"]
            del data["keyv"]
            db.child("thesis_data").child(key).update(data)
            load_data()
            return render_template("form/basic_elements.html",token=token,update="1")
        except: 
            return render_template("form/basic_elements.html",token=token,update="3")   
        #return render_template("form/basic_elements.html")
    
    return redirect(url_for("admin_login"))

@app.route("/delete_thesis",methods=["GET","POST"])
def delete_thesis():
    if request.method == "POST":
        try:
            data = dict(request.form)
            key = data["key"]
            label = value[key]["Label"]
            db.child("thesis_data").child(key).remove()
            storage.delete(label)
            load_data()
            return "200"
        except:
            return "500"    
    return redirect(url_for("admin_login"))

@app.route("/form")
def form():
    load_data()
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)),debug=True,use_reloader=True)