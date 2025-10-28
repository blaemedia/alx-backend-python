import mysql.connector
from mysql.connector import Error
import csv
import uuid

# ------------------------
# 1️⃣ CONNECT TO MYSQL SERVER
# ------------------------
def connect_db():
    """Connects to the MySQL server (without specifying a database)."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",       # change to your MySQL username
            password="password"  # change to your MySQL password
        )
        if connection.is_connected():
            print("✅ Connected to MySQL Server.")
            return connection
    except Error as e:
        print(f"❌ Error while connecting to MySQL: {e}")
        return None


# ------------------------
# 2️⃣ CREATE DATABASE IF NOT EXISTS
# ------------------------
def create_database(connection):
    """Creates the ALX_prodev database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        print("✅ Database 'ALX_prodev' is ready.")
    except Error as e:
        print(f"❌ Error while creating database: {e}")


# ------------------------
# 3️⃣ CONNECT TO ALX_prodev DATABASE
# ------------------------
def connect_to_prodev():
    """Connects directly to the ALX_prodev database."""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="ALX_prodev"
        )
        if connection.is_connected():
            print("✅ Connected to 'ALX_prodev' database.")
            return connection
    except Error as e:
        print(f"❌ Error connecting to ALX_prodev: {e}")
        return None


# ------------------------
# 4️⃣ CREATE TABLE user_data IF NOT EXISTS
# ------------------------
def create_table(connection):
    """Creates the user_data table with the required fields."""
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            age DECIMAL(5,2) NOT NULL,
            INDEX (user_id)
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("✅ Table 'user_data' is ready.")
    except Error as e:
        print(f"❌ Error while creating table: {e}")


# ------------------------
# 5️⃣ INSERT DATA FROM CSV FILE
# ------------------------
def insert_data(connection, data):
    """Inserts data into the user_data table if it doesn't already exist."""
    try:
        cursor = connection.cursor()
        check_query = "SELECT COUNT(*) FROM user_data WHERE email = %s"
        insert_query = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
        
        for row in data:
            cursor.execute(check_query, (row['email'],))
            exists = cursor.fetchone()[0]
            if exists == 0:
                cursor.execute(insert_query, (str(uuid.uuid4()), row['name'], row['email'], row['age']))
        connection.commit()
        print("✅ Data inserted successfully.")
    except Error as e:
        print(f"❌ Error inserting data: {e}")


# ------------------------
# 6️⃣ GENERATOR FUNCTION TO STREAM ROWS
# ------------------------
def stream_user_data(connection):
    """Yields rows one by one from the user_data table."""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    for row in cursor:
        yield row


# ------------------------
# 7️⃣ MAIN SCRIPT EXECUTION
# ------------------------
if __name__ == "__main__":
    # Step 1: Connect to MySQL
    conn = connect_db()
    if conn:
        create_database(conn)
        conn.close()

    # Step 2: Connect to ALX_prodev
    db_conn = connect_to_prodev()
    if db_conn:
        create_table(db_conn)

        # Step 3: Read data from CSV
        try:
            with open("user_data.csv", "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                data = [row for row in reader]
                insert_data(db_conn, data)
        except FileNotFoundError:
            print("❌ user_data.csv file not found.")

        # Step 4: Stream data
        print("\n📤 Streaming rows from database:")
        for user in stream_user_data(db_conn):
            print(user)

        db_conn.close()

