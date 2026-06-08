import os
import sqlite3
def create_db():
    # os.path.isfile checks if the path exists AND is a file (not a folder)
    if os.path.isfile('inv.db'):
        return
    else:
        print('ye')

    conn = sqlite3.connect('inv.db')
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON;')
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, discord_id TEXT UNIQUE, username TEXT, display_name TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS conditions (id INTEGER PRIMARY KEY, label TEXT UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS storage_locations (id INTEGER PRIMARY KEY, label TEXT UNIQUE)')
    cursor.execute('CREATE TABLE IF NOT EXISTS category (id INTEGER PRIMARY KEY, label TEXT UNIQUE)')
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        name TEXT,
        condition_id INTEGER,
        storage_id INTEGER,
        category_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (condition_id) REFERENCES conditions (id),
        FOREIGN KEY (storage_id) REFERENCES storage_locations (id),
        FOREIGN KEY (category_id) REFERENCES category (id)
        )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS category_details_type
                (id INTEGER PRIMARY KEY,
                category_id INTEGER,
                LABEL TEXT,
                FOREIGN KEY (category_id) REFERENCES category (id)
                )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS category_details
                (id INTEGER PRIMARY KEY,
                detail_id INTEGER,
                item_id INTEGER,
                Description TEXT,
                FOREIGN KEY (detail_id) REFERENCES category_details_type (id),
                FOREIGN KEY (item_id) REFERENCES items (id)
                )''')
    # cursor.execute("INSERT INTO users VALUES ('Tobias', 28)")
    conn.commit()