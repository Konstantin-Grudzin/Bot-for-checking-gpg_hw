
import json
import os
from pathlib import Path


path = Path(__file__)
default_path = str(path.parent)+("/user/")

def reWriteFile(data,file):
    txt = json.dumps(data,indent=4)
    file.truncate(0)
    file.seek(0)
    file.write(txt)

def userExist(id):
    return os.path.exists(default_path+f"{id}.json")

def getUserJson(id):
    with open(default_path+f"{id}.json",'r') as file:
        return json.load(file)

def writeUserJson(id, data):
    print("write str1:",data)
    with open(default_path+f"{id}.json",'w') as file:
        reWriteFile(data,file)

def changeState(id,state):
    with open(default_path+f"{id}.json",'r+') as file:
        data = json.load(file)
        data["state"] = state.value
        reWriteFile(data,file)

def changeName(id,name):
    with open(default_path+f"{id}.json",'r+') as file:
        data = json.load(file)
        data["username"] = name
        reWriteFile(data,file)

def changeResult(id):
    with open(default_path+f"{id}.json",'r+') as file:
        data = json.load(file)
        data["result"] = True
        reWriteFile(data,file)