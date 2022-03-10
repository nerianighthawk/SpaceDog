import sqlite3

db_name = 'SPACEDOG.db'


def add_member(content_list, user_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    for content in content_list:
        cur.execute(f'INSERT INTO contents(discord_id, content) values({user_id}, "{content}")')

    conn.commit()

    cur.close()
    conn.close()


def read_contents(user_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute(f'SELECT * FROM contents WHERE discord_id={user_id}')
    contents_list = cur.fetchall()

    cur.close()
    conn.close()

    return contents_list


def delete_contents(user_id):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    cur.execute(f'DELETE FROM contents WHERE discord_id={user_id}')

    cur.close()
    conn.close()


def init_setting():
    conn = sqlite3.connect(db_name)
    
    cur = conn.cursor()
    cur.execute('CREATE TABLE contents(id INTEGER PRIMARY KEY AUTOINCREMENT, discord_id INTEGER, content STRING)')

    conn.commit()

    cur.close()
    conn.close()
