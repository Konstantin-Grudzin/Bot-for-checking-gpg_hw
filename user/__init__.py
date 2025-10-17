from sql_helper import SQL
from user_helper import UserState


class User:
    instance: dict[int, "User"] = {}

    def __new__(cls, id):
        cls.sql = SQL()
        if id not in cls.instance:
            print(f"USER {id} IS BORN")
            cls.instance[id] = object.__new__(cls)
            cls.sql.create_user(id)
        return cls.instance[id]

    def __init__(self, id):
        self.id = id
        self.state = UserState(self.sql.get_state(id))
        self.result = self.sql.get_result(id)
        self.name = self.sql.get_name(id)
        self.group = self.sql.get_group(id)

    def change_state(self, state: UserState):
        self.state = state
        self.sql.set_state(self.id, self.state.value)

    def set_exam_info(self, name):
        self.name = name[0]
        self.group = name[1]
        self.sql.set_name(self.id, self.name)
        self.sql.set_group(self.id, self.group)

    def change_result(self):
        self.result = True
        self.sql.set_passed(self.id)
