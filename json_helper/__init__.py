from io import TextIOWrapper
import json
from pathlib import Path


class JSON:
    instance = None
    file: TextIOWrapper = None
    json_data = None

    def __new__(cls, path: Path | None = None):
        if cls.instance is None:
            print("JSON IS BORN")
            cls.instance = object.__new__(cls)

            data = {"user": -1, "offset": 0}
            if not path.exists():
                with open(path,'w') as file:
                    file.write(json.dumps(data,indent=4,ensure_ascii=False))
            
            cls.file = open(path, 'r+')
            cls.json_data = json.loads(cls.file.read())
        return cls.instance
    
    def get_offset(self):
        return self.json_data["offset"]
    
    def set_offset(self, offset: int):
        self.json_data["offset"] = offset

    def get_user(self):
        return self.json_data["user"]
    
    def set_user(self, offset: int):
        self.json_data["user"] = offset

    def close(self):
        self.file.truncate(0)
        self.file.seek(0)
        self.file.write(json.dumps(self.json_data,indent=4,ensure_ascii=False))
        self.file.close()