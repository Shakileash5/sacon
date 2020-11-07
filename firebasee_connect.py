import pyrebase
import requests
import json

config = {
  "apiKey": "AIzaSyA_DAsVDs2wNv2glJ9hE5KPMNc4tygdDf0",
  "authDomain": "sacon-search.firebaseapp.com",
  "databaseURL": "https://sacon-search.firebaseio.com/",
  "storageBucket": "sacon-search.appspot.com",
  "serviceAccount": "Credentials/sacon-search-firebase-adminsdk-yq4jc-4bc5493504.json"
}

firebase = pyrebase.initialize_app(config_)
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

data = {'Author': 'Singh, P.', 'Year': '2014', 'University': 'Forest Research Institute, Dehradun', 'Title': 'Study of altitudinal and geographical song variation, and interspecific interaction among Phylloscopus warblers in the Himalayas', 'Keywords': ['Leaf warblers', 'Phylloscopus xanthoschistos', 'Phylloscopus reguloides', 'Phylloscopidae', 'Western Himalayas', 'Eastern Himalaya', 'North-eastern Hills', 'Forests', 'Behavioural ecology', 'Avian vocalization', 'Competition', 'Habitat selection'], 'Label': 'TD-00010.docx', 'Type': 'Ph.D.', 'Academic department': 'Wildlife Institute of India', 'No of pages': ''}

d = json.dumps(data)
print(d)
db.child("thesis_data").child("17537157278").update(data)

#val = dict(db.child("thesis_data").get().val())
#print(val)
#keys = val.keys()



#value = dict(db.child("thesis_data").get().val())
#print(value)
storage = firebase.storage()
#myfile = storage.child("TD-000104.pdf")
#url = myfile.get_url(None)
#durl = myfile.get_url("a2ed4099-d8a3-4966-887f-da303739ab49")
#print(url,durl)



#myfile = storage.child("TD-00001.pdf")
#url = myfile.get_url(None)
#print(url)
#storage.child("TD-00171.pdf").put("TD-00171.pdf")
#res = requests.get(url, allow_redirects=True)
#print(res.headers.get('content-type'))
#open("static/TD-000005.pdf", 'wb').write(res.content)


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