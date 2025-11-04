import sqlite3

# 1️⃣ Custom class-based context manager
class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = None

    def __enter__(self):
        """Open database connection when entering the 'with' block"""
        self.conn = sqlite3.connect(self.db_name)
        print(f"Connected to database: {self.db_name}")
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        """Close connection automatically when leaving the 'with' block"""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        # Returning False means exceptions (if any) will still be raised
        return False


# 2️ Use the context manager
with DatabaseConnection("database.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print("Query results:", results)
