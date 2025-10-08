from secret_info import adminUsers

def canPass(id):
    global adminUsers
    return id in adminUsers