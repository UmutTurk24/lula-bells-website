import mysql.connector
import bcrypt

###############################
####  Production Functions ####
###############################


def guest_connect_to_database(username, password, host, database):
    """Connects to the database and returns the connection object"""

    try:
        connection = mysql.connector.connect(
            user='guest', password='guest', host=host, database=database
        )
        cursor = connection.cursor()
        print("Connected to database")
        return connection, cursor
    except mysql.connector.Error as error_descriptor:
        print("Failed connecting to database: {}".format(error_descriptor))
        return mysql.connector.Error


def check_authentication(_connection, cursor, username, password):
    """Check if the username and password are valid"""

    try:
        # Check if the username exists
        cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
        if cursor.fetchone() is None:
            return False

        # Retrieve the password from the database
        cursor.execute(
            "SELECT password FROM Users WHERE username = %s", (username,)
        )
        db_password = cursor.fetchone()[0]

        if bcrypt.checkpw(password.encode('utf-8'), db_password.encode('utf-8')):
            return True

        return False
    except mysql.connector.Error as error_descriptor:
        print("Failed connecting to database: {}".format(error_descriptor))
        return mysql.connector.Error


def create_user(connection, cursor, username, password):
    """Create a new user in the database"""

    # Check if the username already exists
    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    if cursor.fetchone() is not None:
        return False

    # Create a salt
    salt = bcrypt.gensalt()

    # Hash the password with the salt
    password = bcrypt.hashpw(password.encode(), salt)

    # Insert the new user into the database

    try:
        cursor.execute(
            "INSERT INTO Users (username, password, salt) VALUES (%s, %s, %s)",
            (username, password, salt),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Textbooks item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        return mysql.connector.Error

    return True
