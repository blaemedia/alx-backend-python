import sqlite3 
import functools
from datetime import datetime  

def with_db_connection(func):
    """Decorator to manage database connection."""
    # Decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Assume the query is passed as a keyword argument or positional argument
        query = kwargs.get('query') or (args[0] if args else None)
        if query:
            print(f"[{datetime.now()}] Executing SQL query: {query}")  # Log the query
        return func(*args, **kwargs)  # Call the original function
    return wrapper

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)