from secret_info import adminUsers


def can_pass(id):
    global adminUsers
    return id in adminUsers
