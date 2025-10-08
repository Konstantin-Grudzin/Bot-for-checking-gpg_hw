from pathlib import Path
import json
import AdminPanel
import JsonHelper
import TgHandler
from UserMaster.UserMaster import ProcessMessage

path = Path(__file__)
dataLoc = str(path.parent)+("/data.json")

def main():
    print("===start===")
    with open(dataLoc,'r+') as file:
        dataJson = json.load(file)
        AdminPanel.SetData(dataJson)
        while True:
            [messages,dataJson["offset"]]=TgHandler.getUpdates(dataJson["offset"])
            for message in messages["result"]:
                print(message)
                messageType = [*message.keys()][1]
                message=message[messageType]
                if(not message.get("text",None) is None):
                    ProcessMessage(message)
                else:
                    print("I can't handle this")
                
            #TODO: Enable SIGKILL message and move this block from while
            JsonHelper.reWriteFile(dataJson,file)
            AdminPanel.Notify()
            print("===HeartBeat===")
    
if __name__ == "__main__":
    main()
