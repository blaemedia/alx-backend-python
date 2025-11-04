import time
import sqlite3
import functools

# 1️⃣ Dictionary to store cached query results
query_cache = {}

# 2️⃣ Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if query is already in cache
        if query in query_cache:
            print(f"Using cached result for query: {query}")
            return query_cache[query]
        
        # If not cached, execute the function and store the result
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print(f"Caching result for query: {query}")
        return result
    return wrapper

# 3️⃣ Example with database connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect("database.db")  # change DB name if needed
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

# 4️⃣ Decorated function
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# 5️⃣ Test caching
users = fetch_users_with_cache(query="SELECT * FROM users")
users_again = fetch_users_with_cache(query="SELECT * FROM users")
