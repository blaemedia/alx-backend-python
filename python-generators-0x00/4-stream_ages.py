import mysql.connector

def connect_to_prodev():
    """Connect to the ALX_prodev database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="ALX_prodev"
    )


def stream_user_ages():
    """Generator that streams user ages one by one."""
    connection = connect_to_prodev()
    cursor = connection.cursor()

    cursor.execute("SELECT age FROM user_data")

    # ✅ yields one age at a time, keeping memory use low
    for (age,) in cursor:
        yield float(age)

    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculates and prints the average age using the generator."""
    total = 0
    count = 0

    # ✅ first loop: iterates through generator
    for age in stream_user_ages():
        total += age
        count += 1

    # ✅ no second loop — simple division
    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")


if __name__ == "__main__":
    calculate_average_age()

