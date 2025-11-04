import sqlite3
import functools

# Decorator to handle database connection
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect("database.db")  # change DB name as needed
        try:
            # Pass connection as first argument to the function
            return func(conn, *args, **kwargs)
        finally:
            # Close the connection after function completes
            conn.close()
    return wrapper

# Decorated function
@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user
user = get_user_by_id(user_id=1)
print(user)
