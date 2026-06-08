import sqlite3

def insert_item(user_id,
                name,
                condition = 'unknown',
                storage = 'unknown',
                category = 'misc'):
    conn = sqlite3.connect('inv.db')
    cursor = conn.cursor()
    
    cursor.execute('INSERT OR IGNORE INTO category (label) VALUES (?);',(category,))
    cursor.execute('SELECT id FROM category WHERE label = ?;', (category,))
    category_id = cursor.fetchone()[0]
    cursor.execute('INSERT OR IGNORE INTO storage_locations (label) VALUES (?);',(storage,))
    cursor.execute('SELECT id FROM storage_locations WHERE label = ?;', (storage,))
    storage_id = cursor.fetchone()[0]
    cursor.execute('INSERT OR IGNORE INTO conditions (label) VALUES (?);',(condition,))
    cursor.execute('SELECT id FROM conditions WHERE label = ?;', (condition,))
    condition_id = cursor.fetchone()[0]
    cursor.execute('''
        INSERT INTO items (user_id, name, condition_id, storage_id, category_id) 
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, name, condition_id, storage_id, category_id))

    conn.commit()
    conn.close() 

def get_items(discord_id):
    conn = sqlite3.connect('inv.db')
    cursor = conn.cursor()
    cursor.execute('select * FROM items where user_id = (SELECT id FROM users where discord_id = ?)',(discord_id,))
    results = cursor.fetchall()
    conn.close() 
    return results