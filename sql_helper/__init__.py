from pathlib import Path
import sqlite3


class SQL:
    instance = None
    connect = None
    cursor = None
    def __new__(cls, path: Path | None = None):
        if cls.instance is None:
            print("SQL IS BORN")
            cls.instance = object.__new__(cls)
            cls.connect = sqlite3.connect(path)
            cls.cursor = cls.connect.cursor()

            cls.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Passed (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER
                )
            """)

            cls.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Dump (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    json TEXT
                )
            """)

            cls.cursor.execute("""
                CREATE TABLE IF NOT EXISTS User (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    name TEXT,
                    "group" TEXT,
                    state INTEGER,
                    passed BOOLEAN,
                    fingerprint TEXT
                )
            """)

            cls.connect.commit()
        return cls.instance

    def create_user(self,id):
        self.cursor.execute("SELECT * FROM User WHERE user_id = ?", (id,))
        if self.cursor.fetchone() is None:
            self.cursor.execute("""
                INSERT INTO User (user_id, name, "group", state, passed, fingerprint)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id, "", "", 0, False, ""))
            self.connect.commit()

    def get_state(self, id):
        self.cursor.execute("SELECT state FROM User WHERE user_id = ?", (id,))
        row = self.cursor.fetchone()
        return row[0] if row else 0
    
    def get_result(self, id):
        self.cursor.execute("SELECT passed FROM User WHERE user_id = ?", (id,))
        row = self.cursor.fetchone()
        return row[0] if row else False
    
    def get_name(self, id):
        self.cursor.execute("SELECT name FROM User WHERE user_id = ?", (id,))
        row = self.cursor.fetchone()
        return row[0] if row else None
    
    def get_group(self, id):
        self.cursor.execute("SELECT \"group\" FROM User WHERE user_id = ?", (id,))
        row = self.cursor.fetchone()
        return row[0] if row else None
    
    def get_fingerprint(self, id):
        self.cursor.execute("SELECT fingerprint FROM User WHERE user_id = ?", (id,))
        row = self.cursor.fetchone()
        return row[0] if row else None
    
    def set_name(self, user_id: int, name: str):
        self.cursor.execute('UPDATE User SET name = ? WHERE user_id = ?', (name, user_id,))
        self.connect.commit()

    def set_group(self, user_id: int, group: str):
        self.cursor.execute('UPDATE User SET "group" = ? WHERE user_id = ?', (group, user_id,))
        self.connect.commit()

    def set_state(self, user_id: int, state: int):
        self.cursor.execute('UPDATE User SET state = ? WHERE user_id = ?', (state, user_id,))
        self.connect.commit()

    def set_passed(self, user_id: int):
        self.cursor.execute('UPDATE User SET passed = ? WHERE user_id = ?', (True, user_id,))
        self.cursor.execute('INSERT  INTO Passed (user_id) VALUES (?)', (user_id,))
        self.connect.commit()

    def set_fingerprint(self, user_id: int, fingerprint: str):
        self.cursor.execute('UPDATE User SET fingerprint = ? WHERE user_id = ?', (fingerprint, user_id,))
        self.connect.commit()
    
    def get_list_of_all_passed(self):
        self.cursor.execute("""
                            SELECT User.name, User."group"
                            FROM User
                            INNER JOIN Passed ON User.user_id = Passed.user_id
                            """)
        rows = self.cursor.fetchall()
        return [name+" "+group for name, group in rows]
    
    def insert_message(self,id,message):
        self.cursor.execute('INSERT  INTO Dump (user_id, json) VALUES (?,?)', (id,message,))
        self.connect.commit()
    
    def get_new_passed_user(self, id):
        self.cursor.execute("""
                            SELECT Passed.id, User.name, User."group"
                            FROM Passed
                            JOIN User ON Passed.user_id = User.user_id
                            WHERE Passed.id > ?
                            ORDER BY Passed.id ASC
                            LIMIT 1
                            """, (id,))
        row = self.cursor.fetchone()
        return row if row else (None,None,None)


    def close(self):
        self.connect.close()
    

    
