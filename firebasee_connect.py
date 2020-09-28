import pyrebase
import requests

config = {
  "apiKey": "AIzaSyDLYsJm85_J4D0rKZ0TLLMAM-3orCXGE6A",
  "authDomain": "sacon-250805.firebaseapp.com",
  "databaseURL": "https://sacon-250805.firebaseio.com/",
  "storageBucket": "sacon-250805.appspot.com",
  "serviceAccount": "Credentials/sacon-250805-firebase-adminsdk-cc9yo-7d68092103.json"
}
firebase = pyrebase.initialize_app(config)
#auth = firebase.auth()

#user = auth.sign_in_with_email_and_password("shakileash2000@gmail.com","sugishaki1")
#print(user.keys())
db = firebase.database()
keywords = ["Rails",
"Porphyrio porphyrio",
"Rallidae",
"Malabar Plains",
"Wetlands",
"Species ecology & life-history strategies",
"Bird populations",
"Species abundance",
"Microhabitat characteristics",
"Breeding success"]

data = {"Author": "E. V. Abdulla", "Year": 2006,"University":"Farook College","Title":"Biology, ecology and behaviour of Purple Moorhen Porphyrio porphyrio","Keywords":keywords,"Label":"TD-00022","Type":"Ph.D."}

#db.child("thesis_data").push(data)
value = dict(db.child("thesis_data").get().val())
#print(value)
storage = firebase.storage()
myfile = storage.child("TD-000005.pdf")
#storage.child("TD-000171.docx").download("templates","TD-000171.docx")
url = myfile.get_url(None)
print(url)
res = requests.get(url, allow_redirects=True)
print(res.headers.get('content-type'))
open("static/TD-000005.pdf", 'wb').write(res.content)


'''find = "Rallidae"
keys = value.keys()
for key in keys:
    gets = value[key].values()
    for get in gets:
        if isinstance(get, str) :
            #print(find in get)
            if find in get:
                print(find)
        elif isinstance(get, list):
            for l in get:
                if find in l:
                    print(find)
        elif isinstance(get, int):
            if find ==  get:
                print(find)     '''                 