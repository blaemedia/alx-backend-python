import sqlite3

class ExecuteQuery:
    def __init__(self, query, params=()):
        self.query = query          # SQL query string
        self.params = params        # Query parameters (tuple)
        self.conn = None            # Will hold the database connection
        self.cursor = None          # Will hold the cursor
        self.results = None         # Will hold query results

    def __enter__(self):
        """Opens the database connection and executes the query."""
        self.conn = sqlite3.connect("users.db")
        self.cursor = self.conn.cursor()
        print(f"Executing query: {self.query} | Params: {self.params}")
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results  # Return results directly for use inside 'with'

    def __exit__(self, exc_type, exc_value, traceback):
        """Closes the connection safely."""
        if self.conn:
            self.conn.close()
        if exc_type:
            print(f"An error occurred: {exc_value}")
        return False  # Propagate exceptions if they occur
