import mysql.connector
import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

SCHEMA_FILE = os.path.join(CURRENT_DIR, "db_schema.sql")
DYNAMIC_FILE = os.path.join(CURRENT_DIR, "db_dynamics.sql")

TEST_DB_NAME = "TestLulaBells"
TEST_SCHEMA_FILE = os.path.join(CURRENT_DIR, "test_db_schema.sql")
TEST_DYNAMIC_FILE = os.path.join(CURRENT_DIR, "database/test_db_dynamics.sql")


###############################
####  Set Up Connection    ####
###############################

def connect_to_database_provider():
    """Connects to the database provider and returns the connection object"""

    try:
        connection = mysql.connector.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )

        return connection
    except mysql.connector.Error as error_descriptor:
        print("Failed connecting to database: {}".format(error_descriptor))
        exit(1)


###############################
####  Set Up DB Connection ####
###############################


def connect_to_database():
    """Connects to the database and returns the connection object"""

    try:
        connection = mysql.connector.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME
        )

        return connection
    except mysql.connector.Error as error_descriptor:
        print("Failed connecting to database: {}".format(error_descriptor))
        exit(1)


def connect_to_test_database():
    """Connects to the database and returns the connection object"""

    try:
        # Create the test database
        connection = mysql.connector.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = connection.cursor()

        cursor.execute("DROP DATABASE IF EXISTS {}".format(TEST_DB_NAME))
        connection.commit()

        cursor.execute("CREATE DATABASE {}".format(TEST_DB_NAME))
        connection.commit()

        cursor.close()
        connection.close()

        # Connect to the test database
        connection = mysql.connector.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=TEST_DB_NAME
        )
        cursor = connection.cursor()
        return connection, cursor
    except mysql.connector.Error as error_descriptor:
        print("Failed connecting to database: {}".format(error_descriptor))
        exit(1)


#################################
###### Database Creation ########
#################################


def create_database(cursor):
    """Creates the database"""

    try:
        # Drop the database if it exists
        cursor.execute("DROP DATABASE IF EXISTS {}".format(DB_NAME))

        # Create the database
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME)
        )
    except mysql.connector.Error as error_descriptor:
        print("Failed creating database: {}".format(error_descriptor))
        exit(1)


def create_test_database(cursor):
    """Creates the test database"""

    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(TEST_DB_NAME)
        )
    except mysql.connector.Error as error_descriptor:
        print("Failed creating database: {}".format(error_descriptor))
        exit(1)


#################################
###### Schema Insertion #########
#################################


def build_schema(connection, cursor):
    """Builds the database schema"""

    file = open(SCHEMA_FILE, "r")
    file_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(file_string, multi=True):
            pass
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed creating database: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def build_test_schema(connection, cursor):
    """Builds the database schema"""

    file = open(TEST_SCHEMA_FILE, "r")
    file_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(file_string, multi=True):
            pass
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed creating database: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def build_dynamic(connection, cursor):
    """Builds the database schema"""

    file = open(DYNAMIC_FILE, "r")
    file_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(file_string, multi=True):
            pass
    except mysql.connector.Error as error_descriptor:
        print("Failed creating database: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def build_test_dynamic(connection, cursor):
    """Builds the database schema"""

    file = open(TEST_DYNAMIC_FILE, "r")
    file_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(file_string, multi=True):
            pass
    except mysql.connector.Error as error_descriptor:
        print("Failed creating database: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)




#################################
#######   MAIN TESTING  #########
#################################


def main():
    connection = connect_to_database()
    cursor = connection.cursor()
    build_schema(connection, cursor)
    build_dynamic(connection, cursor)
    connection.commit()
    cursor.close()
    connection.close()


# export main
if __name__ == "__main__":
    main()
