from .base import connect_db, commit_and_close


def check_user_exists(db_name, username):
    connection, cursor = connect_db(db_name)
    cursor.execute("SELECT * FROM users WHERE username = ?;", (username,))
    user = cursor.fetchone() # (), None
    if not user:
        return False, False  # (False, False)
    return True, user[0]


def add_user(db_name, username):
    connection, cursor = connect_db(db_name)
    cursor.execute("INSERT INTO users(username) VALUES (?);", (username,))
    commit_and_close(connection)
    print(username, 'added')


def add_weather(db_name, **kwargs):
    connection, cursor = connect_db(db_name)
    keys = ', '.join([key for key in kwargs.keys()])
    values = tuple(kwargs.values())
    chars = ', '.join(['?' for _ in range(len(kwargs.keys()))])
    cursor.execute(f"INSERT INTO weather({keys}) VALUES ({chars});", values)
    commit_and_close(connection)


def get_user_history(db_name, user_id):
    connection, cursor = connect_db(db_name)
    sql = "SELECT * FROM weather WHERE user_id = ?;"
    cursor.execute(sql, (user_id,))
    return cursor.fetchall()


def clear_history(db_name, user_id):
    connection, cursor = connect_db(db_name)
    sql = "DELETE FROM weather WHERE user_id = ?"
    cursor.execute(sql, (user_id,))
    commit_and_close(connection)
