import mysql.connector

DB_USER = "root"
DB_PASSWORD = "123456"
DB_HOST = "localhost"
DB_NAME = "LulaBells"


SCHEMA_FILE = "database/db_schema.sql"
DYNAMIC_FILE = "database/db_dynamics.sql"

TEST_DB_NAME = "TestLulaBells"
TEST_SCHEMA_FILE = "database/test_db_schema.sql"
TEST_DYNAMIC_FILE = "database/test_db_dynamics.sql"


###############################
####  Set Up Connection    ####
###############################

def connect_to_database_provider():
    """Connects to the database provider and returns the connection object"""

    try:
        connection = mysql.connector.connect(
            user=DB_USER, password=DB_PASSWORD, host=DB_HOST
        )
        cursor = connection.cursor()
        return connection, cursor
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
        cursor = connection.cursor()
        return connection, cursor
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
    schema_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(schema_string, multi=True):
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
    schema_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(schema_string, multi=True):
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
    schema_string = file.read()
    file.close()

    try:
        for _ in cursor.execute(schema_string, multi=True):
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
    connection, cursor = connect_to_database_provider()
    build_test_schema(connection, cursor)
    connection.commit()
    cursor.close()
    connection.close()


# export main
if __name__ == "__main__":
    main()

# Export build_schema

# Export connect_to_database
