import mysql.connector
import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # This is your Project Root

SCHEMA_FILE  = os.path.join(CURRENT_DIR, "db_schema.sql")
DYNAMIC_FILE = os.path.join(CURRENT_DIR, "db_dynamics.sql")

TEST_DB_NAME = "TestLulaBells"
TEST_SCHEMA_FILE  =  os.path.join(CURRENT_DIR, "test_db_schema.sql")
TEST_DYNAMIC_FILE = os.path.join(CURRENT_DIR,"database/test_db_dynamics.sql")


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
###### Data Insertion ###########
#################################


def add_test_data(connection, cursor):
    """Adds test data to the database"""

    try:
        # Insert data into Students table
        students_data = [
            (801396000, "Kerem", "King", 2026, 1, "2020-01-01"),
            (801396001, "Idil", "Rara", 2026, 1, "2021-01-01"),
            (801396002, "Baris", "Kalay", 2026, 1, "2022-01-01"),
            (801396003, "Iasa", "Hatata", 2026, 1, "2022-01-01"),
        ]
        cursor.executemany(
            "INSERT INTO Students (student_id, student_name, student_surname, class_year, residence, registration_date) VALUES (%s, %s, %s, %s, %s, %s)",
            students_data,
        )

        # Insert data into Pantry table
        pantry_data = [("Yogurt", 2), ("Potato", 10), ("Onions", 20)]
        cursor.executemany(
            "INSERT INTO Pantry (item_name, quantity) VALUES (%s, %s)", pantry_data
        )

        # Insert data into PantryPurchase table
        pantry_purchase_data = [
            (801396000, "Yogurt", "2023-05-05", 4),
            (801396000, "Potato", "2023-05-05", 4),
            (801396000, "Potato", "2023-05-04", 4),
            (801396000, "Yogurt", "2023-05-04", 4),
            (801396001, "Yogurt", "2023-05-05", 10),
            (801396001, "Onions", "2023-05-05", 10),
            (801396002, "Potato", "2023-05-05", 5),
        ]
        cursor.executemany(
            "INSERT INTO PantryPurchase (student_id, item_name, purchase_date, quantity) VALUES (%s, %s, %s, %s)",
            pantry_purchase_data,
        )

        # Insert data into Wardrobe table
        wardrobe_data = [("CL_10",), ("CL_11",)]
        cursor.executemany("INSERT INTO Wardrobe (cloth_id) VALUES (%s)", wardrobe_data)

        # Insert data into WardrobeRentals table
        wardrobe_rentals_data = [
            (801396000, "CL_10", "2023-05-05", "2023-05-15", 0, "Bad customer", "Umo"),
            (801396001, "CL_11", "2023-05-10", "2023-05-15", 0, "Bad customer", "Umo"),
        ]
        cursor.executemany(
            "INSERT INTO WardrobeRentals (student_id, cloth_id, rental_date, due_date, is_returned, notes, renter_info) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            wardrobe_rentals_data,
        )

        # Commit the transaction
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed adding test data: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


#################################
#######   MAIN TESTING  #########
#################################

def main():
    connection, cursor = connect_to_database()
    build_schema(connection, cursor)
    build_dynamic(connection, cursor)
    add_test_data(connection, cursor)
    connection.commit()
    cursor.close()
    connection.close()


# export main
if __name__ == "__main__":
    main()
