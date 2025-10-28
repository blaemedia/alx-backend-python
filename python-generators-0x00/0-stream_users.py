import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator that streams rows one by one from the user_data table."""
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # change to your MySQL username
            password="password",  # change to your MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            # 🔁 Use only one loop (requirement)
            for row in cursor:
                yield row

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        # Close connection cleanly
        if connection.is_connected():
            cursor.close()
            connection.close()

##🧠 Usage Example
for user in stream_users():
    print(user)

