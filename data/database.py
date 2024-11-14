import sqlite3

class Database:
    def __init__(self, db_name="data/dbData.db"):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS messages (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                message TEXT,
                                encrypted_message TEXT,
                                hash INTEGER)''')
        self.connection.commit()

    def save_message(self, message, encrypted_message, hash_value):
        self.cursor.execute("INSERT INTO messages (message, encrypted_message, hash) VALUES (?, ?, ?)",
                            (message, encrypted_message, hash_value))
        self.connection.commit()

    def get_messages(self):
        self.cursor.execute("SELECT * FROM messages")
        return self.cursor.fetchall()

    def close(self):
        self.connection.close()
