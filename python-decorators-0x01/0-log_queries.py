import sqlite3 
import functools

def with_db_connection(func):
    """Decorator to manage database connection."""
    def wrapper(*args, **kwargs):
        # Expect the first argument to be the connection
        conn = args[0]  
        cursor = conn.cursor()
        
        # Replace the connection in args with a custom cursor wrapper
        class CursorLogger:
            def __init__(self, cursor):
                self.cursor = cursor

            def execute(self, query, params=()):
                print(f"Executing SQL: {query} | Params: {params}")  # Log query
                return self.cursor.execute(query, params)

            def __getattr__(self, name):
                # Delegate other attributes/methods to the real cursor
                return getattr(self.cursor, name)

        # Replace original cursor with logging cursor
        args = (CursorLogger(cursor), *args[1:])
        return func(*args, **kwargs)
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)