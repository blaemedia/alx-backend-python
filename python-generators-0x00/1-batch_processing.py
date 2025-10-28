
import mysql.connector
from mysql.connector import Error

# -----------------------------
# 1️⃣ Stream users in batches
# -----------------------------
def stream_users_in_batches(batch_size):
    """
    Generator that yields rows from the user_data table in batches.
    Each batch contains up to `batch_size` rows.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # change to your MySQL username
            password="password",  # change to your MySQL password
            database="ALX_prodev"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")

            # Loop 1 — Fetch and yield batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch

    except Error as e:
        print(f"❌ Database error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


# -----------------------------
# 2️⃣ Process each batch
# -----------------------------
def batch_processing(batch_size):
    """
    Processes each batch of users from stream_users_in_batches(batch_size),
    filtering users over the age of 25.
    """
    # Loop 2 — iterate over batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 3 — iterate over users in batch
        filtered_users = [user for user in batch if float(user['age']) > 25]
        yield filtered_users


# -----------------------------
# 3️⃣ Example usage
# -----------------------------
if __name__ == "__main__":
    print("📤 Streaming and processing users in batches...\n")

    for filtered_batch in batch_processing(batch_size=3):
        for user in filtered_batch:
            print(user)
