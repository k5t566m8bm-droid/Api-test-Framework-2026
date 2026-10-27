import sqlite3

class DBClient:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, job TEXT)''')
        self.conn.commit()

    def insert(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.lastrowid

    def delete(self, sql, params=()):
        self.cursor.execute(sql, params)
        self.conn.commit()
        return self.cursor.rowcount

    def query_one(self, sql, params=()):
        self.cursor.execute(sql, params)
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()