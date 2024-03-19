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
            (801396000, "Kerem", "King", 2026, 1, "2020-01-01", 0, "Cool student"),
            (801396001, "Idil", "Rara", 2026, 1, "2021-01-01", 0, "Cool student"),
            (801396002, "Baris", "Kalay", 2026, 1, "2022-01-01", 0, "Cool student"),
            (801396003, "Iasa", "Hatata", 2026, 1, "2022-01-01", 0, "Cool student"),
            (801396004, "Emily", "Johnson", 2025, 2, "2021-09-15", 0, "Cool student"),
            (
                801396005,
                "Michael",
                "Williams",
                2024,
                1,
                "2023-02-28",
                0,
                "Cool student",
            ),
            (801396006, "Sophia", "Brown", 2023, 2, "2020-11-10", 0, "Cool student"),
            (801396007, "Daniel", "Jones", 2022, 1, "2021-04-05", 0, "Cool student"),
            (801396008, "Olivia", "Davis", 2026, 1, "2022-07-20", 0, "Cool student"),
            (801396009, "James", "Miller", 2025, 1, "2023-09-03", 0, "Cool student"),
            (801396010, "Emma", "Wilson", 2024, 2, "2021-12-18", 0, "Cool student"),
            (
                801396011,
                "Alexander",
                "Martinez",
                2023,
                1,
                "2022-02-14",
                1,
                "Bad student",
            ),
            (801396012, "Ava", "Taylor", 2022, 2, "2021-05-30", 1, "Bad student"),
            (
                801396013,
                "William",
                "Anderson",
                2026,
                1,
                "2022-08-25",
                1,
                "Cool student",
            ),
        ]
        cursor.executemany(
            "INSERT INTO Students (student_id, student_name, student_surname, class_year, residence, registration_date, agreement_signed, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            students_data,
        )

        # Insert data into Pantry table
        pantry_data = [
            ("Yogurt", 2),
            ("Potato", 10),
            ("Onions", 20),
            ("Milk", 3),
            ("Apples", 15),
        ]
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
            (801396003, "Yogurt", "2023-05-06", 6),
            (801396003, "Potato", "2023-05-06", 6),
            (801396004, "Potato", "2023-05-06", 6),
            (801396004, "Yogurt", "2023-05-06", 6),
            (801396005, "Yogurt", "2023-05-07", 12),
            (801396005, "Onions", "2023-05-07", 12),
            (801396006, "Potato", "2023-05-07", 7),
            (801396007, "Milk", "2023-05-08", 1),
            (801396007, "Apples", "2023-05-08", 1),
            (801396008, "Milk", "2023-05-08", 2),
            (801396008, "Apples", "2023-05-08", 2),
            (801396009, "Milk", "2023-05-09", 3),
            (801396009, "Apples", "2023-05-09", 3),
            (801396010, "Milk", "2023-05-09", 4),
            (801396010, "Apples", "2023-05-09", 4),
            (801396011, "Milk", "2023-05-10", 5),
            (801396011, "Apples", "2023-05-10", 5),
            (801396012, "Milk", "2023-05-10", 6),
            (801396012, "Apples", "2023-05-10", 6),
        ]

        cursor.executemany(
            "INSERT INTO PantryPurchase (student_id, item_name, purchase_date, quantity) VALUES (%s, %s, %s, %s)",
            pantry_purchase_data,
        )

        # Insert data into Wardrobe table
        wardrobe_data = [
            ("CL_10",),
            ("CL_11",),
            ("CL_14",),
            ("CL_15",),
            ("CL_16",),
            ("CL_17",),
            ("CL_18",),
            ("CL_19",),
            ("CL_20",),
            ("CL_21",),
            ("CL_22",),
            ("CL_23",),
            ("CL_24",),
            ("CL_25",),
            ("CL_26",),
            ("CL_27",),
            ("CL_28",),
            ("CL_29",),
            ("CL_30",),
            ("CL_31",),
            ("CL_32",),
            ("CL_33",),
        ]
        cursor.executemany("INSERT INTO Wardrobe (cloth_id) VALUES (%s)", wardrobe_data)

        # Insert data into WardrobeRentals table
        wardrobe_rentals_data = [
            (801396004, "CL_14", "2023-05-15", "2023-05-20", 0, "Bad customer", "Umo"),
            (801396005, "CL_15", "2023-05-20", "2023-05-25", 0, "Bad customer", "Umo"),
            (801396006, "CL_16", "2023-05-25", "2023-05-30", 0, "Bad customer", "Umo"),
            (801396007, "CL_17", "2023-06-01", "2023-06-05", 0, "Bad customer", "Umo"),
            (801396008, "CL_18", "2023-06-05", "2023-06-10", 0, "Bad customer", "Umo"),
            (801396009, "CL_19", "2023-06-10", "2023-06-15", 0, "Bad customer", "Umo"),
            (801396010, "CL_20", "2023-06-15", "2023-06-20", 0, "Bad customer", "Umo"),
            (801396011, "CL_21", "2023-06-20", "2023-06-25", 0, "Bad customer", "Umo"),
            (801396012, "CL_22", "2023-06-25", "2023-06-30", 0, "Bad customer", "Umo"),
            (801396007, "CL_23", "2023-07-01", "2023-07-05", 0, "Bad customer", "Umo"),
            (801396008, "CL_24", "2023-07-05", "2023-07-10", 0, "Bad customer", "Umo"),
            (801396008, "CL_25", "2023-07-10", "2023-07-15", 0, "Bad customer", "Umo"),
            (801396009, "CL_26", "2023-07-15", "2023-07-20", 0, "Bad customer", "Umo"),
            (801396009, "CL_27", "2023-07-20", "2023-07-25", 0, "Bad customer", "Umo"),
            (801396009, "CL_28", "2023-07-25", "2023-07-30", 0, "Bad customer", "Umo"),
            (801396009, "CL_29", "2023-08-01", "2023-08-05", 0, "Bad customer", "Umo"),
            (801396009, "CL_30", "2023-08-05", "2023-08-10", 0, "Bad customer", "Umo"),
        ]
        cursor.executemany(
            "INSERT INTO WardrobeRentals (student_id, cloth_id, rental_date, due_date, is_returned, notes, renter_info) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            wardrobe_rentals_data,
        )

        # Insert data into Textbooks table
        textbooks_data = [
            ("Math 101", 1),
            ("Science 101", 1),
            ("History 101", 1),
            ("English 101", 1),
            ("Art 101", 1),
        ]

        cursor.executemany(
            "INSERT INTO Textbooks (book_name, owned_status) VALUES (%s, %s)",
            textbooks_data,
        )

        # Insert data into TextbookRentals table

        textbook_rentals_data = [
            (801396004, "Math 101", "2023-05-15", "2023-05-20", 0, "Bad customer"),
            (801396005, "Science 101", "2023-05-20", "2023-05-25", 0, "Bad customer"),
            (801396006, "History 101", "2023-05-25", "2023-05-30", 0, "Bad customer"),
            (801396007, "English 101", "2023-06-01", "2023-06-05", 0, "Bad customer"),
            (801396008, "Art 101", "2023-06-05", "2023-06-10", 0, "Bad customer"),
            (801396009, "Math 101", "2023-06-10", "2023-06-15", 0, "Bad customer"),
            (801396010, "Science 101", "2023-06-15", "2023-06-20", 0, "Bad customer" ),
            (801396011, "History 101", "2023-06-20", "2023-06-25", 0, "Bad customer" ),
            (801396012, "English 101", "2023-06-25", "2023-06-30", 0, "Bad customer" ),
            (801396007, "Art 101", "2023-07-01", "2023-07-05", 0, "Bad customer" ),
            (801396008, "Math 101", "2023-07-05", "2023-07-10", 0, "Bad customer" ),
            (801396008, "Science 101", "2023-07-10", "2023-07-15", 0, "Bad customer" ),
            (801396009, "History 101", "2023-07-15", "2023-07-20", 0, "Bad customer" ),
            (801396009, "English 101", "2023-07-20", "2023-07-25", 0, "Bad customer" ),
            (801396009, "Art 101", "2023-07-25", "2023-07-30", 0, "Bad customer" ),
            (801396009, "Math 101", "2023-08-01", "2023-08-05", 0, "Bad customer" ),
            (801396009, "Science 101", "2023-08-05", "2023-08-10", 0, "Bad customer" ),
        ]

        cursor.executemany(
            "INSERT INTO TextbookRentals (student_id, book_name, rental_date, due_date, is_returned, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            textbook_rentals_data,
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
