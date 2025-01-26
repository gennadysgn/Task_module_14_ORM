import sqlite3


def initiate_db():
    connection = sqlite3.connect('Products_4.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
    );
    ''')

    connection.commit()
    connection.close()


def add_user(username, email, age):
    connection = sqlite3.connect('Products_4.db')
    cursor = connection.cursor()
    cursor.execute(f'''
    INSERT INTO Users (username, email, age, balance) VALUES('{username}', '{email}', '{age}', 1000)
''')
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect('Products_4.db')
    cursor = connection.cursor()
    check_user = cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
    if check_user.fetchone() is None:
        connection.commit()
        connection.close()
        return False
    else:
        connection.commit()
        connection.close()
        return True


# initiate_db()
# add_user('Andy', 'andy@gmail.com', 25)
# add_user('Bob', 'bob@gmail.com', 28)
# add_user('Kim', 'kim@gmail.com', 32)
# add_user('Nick', 'nick@gmail.com', 23)