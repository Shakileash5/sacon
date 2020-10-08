import pandas as pd
import csv
import numpy as np
import re
import os 
import pyrebase
import requests
import json
import math

config = {
  "apiKey": "AIzaSyA_DAsVDs2wNv2glJ9hE5KPMNc4tygdDf0",
  "authDomain": "sacon-search.firebaseapp.com",
  "databaseURL": "https://sacon-search.firebaseio.com/",
  "storageBucket": "sacon-search.appspot.com",
  "serviceAccount": "Credentials/sacon-search-firebase-adminsdk-yq4jc-4bc5493504.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


unordered_data = pd.read_csv("NOD_TD_upto830_672Abstracts.csv")
#unordered_data.head()

columns = list(unordered_data.columns)

l = 0
move = 0
email = 0

abstract_data = {}
thesis = []
files = []

for file in os.listdir("./Thesis abstracts_upto830"):
  file = file.split(".")[0]
  files.append(file)

files_ex = []
for file in os.listdir("./Thesis abstracts_upto830"):
  files_ex.append(file)

for attr,val in unordered_data.iterrows():
  n = len(val)
  data = {}
  isNan = 0 
  for i in range(n):
    if pd.isnull(val[i]):
      isNan += 1
  if isNan < 10:
    for i in range(n):      
      if i == 10:
        data[columns[i]] = [val[i]]        
      else:
        if columns[i] == "No. of pages":
          data["No of pages"] = val[i]
        elif columns[i] == "Label":
          ind = files.index(val[i])
          data[columns[i]] = files_ex[ind]
          thesis.append(files[ind])
        else:
          data[columns[i]] = val[i]
     
    abstract_data[str(move)] = data
    move = move+1      
  elif isNan == 11:
    abstract_data[str(move-1)]["Keywords"].append(val[1])
 
  l +=1      
print(len(abstract_data))

 


for i in range(len(abstract_data)):
  if i >279 :
    data = abstract_data[str(i)]
    del data["Unnamed: 11"]
    del data["Thesis #"]
    for l in data.keys():
      #print(l,type(data[l]))
      if isinstance(data[l],list):
        if (isinstance(data[l][0],int) or isinstance(data[l][0],float)) and math.isnan(data[l][0]):
          data[l] = " "
      if isinstance(data[l],int) or isinstance(data[l],float):
        #print("inside",l)
        if math.isnan(data[l]):
          data[l] = " "
    print(i)
    db.child("thesis_data").push(data)

for i in range(len(files)):
  if files[i] not in thesis:
    print(files[i],i)


import pprint