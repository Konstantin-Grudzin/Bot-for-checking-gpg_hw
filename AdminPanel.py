import TgHandler

dataJson = None

def SetData(obj):
    global dataJson
    dataJson = obj

def Notify():
    if(len(dataJson["Admins"])==0 or len(dataJson["Good Students"])==0):
        return
    admins = dataJson["Admins"]
    stud = dataJson["Good Students"][-1]
    for [admin,allow] in admins.items():
        if(not allow): continue
        TgHandler.sendText(admin,f"{stud} pass the test,hooray!")
    dataJson["Good Students"].pop()

def AddGoodStudent(username):
    dataJson["Good Students"].append(username)

def AddAdmin(id):
    dataJson["Admins"][str(id)] = True

def DelAdmin(id):
    del dataJson["Admins"][str(id)]

def OnNotify(id):
    dataJson["Admins"][str(id)] = True

def OffNotify(id):
    dataJson["Admins"][str(id)] = False
