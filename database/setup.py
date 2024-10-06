from schema import (
    build_schema,
    build_dynamic,
    create_database,
    connect_to_database,
    connect_to_database_provider,
)

from insertions import insert_user
import bcrypt
import mysql.connector


def setup_database():
    """Set up the database from scratch"""

    connection = connect_to_database_provider()
    cursor = connection.cursor()

    create_database(cursor)

    cursor.close()
    connection.close()

    connection = connect_to_database()
    cursor = connection.cursor()

    build_schema(connection, cursor)
    build_dynamic(connection, cursor)

    cursor.close()
    connection.close()


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

        # Insert data into Clothes table
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
        cursor.executemany("INSERT INTO Clothes (cloth_id) VALUES (%s)", wardrobe_data)

        # Insert data into ClothRentals table
        cloth_rentals_data = [
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
            "INSERT INTO ClothRentals (student_id, cloth_id, rental_date, due_date, is_returned, notes, renter_info) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            cloth_rentals_data,
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
            (801396004, "Math 101", "2023-05-15", "2023-05-20", 1, "Bad customer"),
            (801396005, "Science 101", "2023-05-20", "2023-05-25", 1, "Bad customer"),
            (801396006, "History 101", "2023-05-25", "2023-05-30", 1, "Bad customer"),
            (801396007, "English 101", "2023-06-01", "2023-06-05", 1, "Bad customer"),
            (801396008, "Art 101", "2023-06-05", "2023-06-10", 1, "Bad customer"),
            (801396009, "Math 101", "2023-06-10", "2023-06-15", 1, "Bad customer"),
            (801396010, "Science 101", "2023-06-15", "2023-06-20", 1, "Bad customer"),
            (801396011, "History 101", "2023-06-20", "2023-06-25", 1, "Bad customer"),
            (801396012, "English 101", "2023-06-25", "2023-06-30", 1, "Bad customer"),
            (801396007, "Art 101", "2023-07-01", "2023-07-05", 1, "Bad customer"),
            (801396008, "Math 101", "2023-07-05", "2023-07-10", 1, "Bad customer"),
            (801396008, "Science 101", "2023-07-10", "2023-07-15", 1, "Bad customer"),
            (801396009, "History 101", "2023-07-15", "2023-07-20", 1, "Bad customer"),
            (801396009, "English 101", "2023-07-20", "2023-07-25", 1, "Bad customer"),
            (801396009, "Art 101", "2023-07-25", "2023-07-30", 1, "Bad customer"),
            (801396009, "Math 101", "2023-08-01", "2023-08-05", 1, "Bad customer"),
            (801396009, "Science 101", "2023-08-05", "2023-08-10", 1, "Bad customer"),
        ]

        cursor.executemany(
            "INSERT INTO TextbookRentals (student_id, book_name, rental_date, due_date, is_returned, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            textbook_rentals_data,
        )

        # Insert data into Kitchenware table
        kitchenware_data = [
            ("KW_1",),
            ("KW_2",),
            ("KW_3",),
            ("KW_4",),
            ("KW_5",),
            ("KW_6",),
            ("KW_7",),
            ("KW_8",),
            ("KW_9",),
            ("KW_10",),
        ]

        cursor.executemany(
            "INSERT INTO Kitchenware (kitchenware_id) VALUES (%s)", kitchenware_data
        )

        # Insert data into KitchenwareRentals table
        kitchenware_rentals_data = [
            (801396004, "KW_1", "2023-05-15", "2023-05-20", 1, "Bad customer"),
            (801396005, "KW_2", "2023-05-20", "2023-05-25", 1, "Bad customer"),
            (801396006, "KW_3", "2023-05-25", "2023-05-30", 1, "Bad customer"),
            (801396007, "KW_4", "2023-06-01", "2023-06-05", 1, "Bad customer"),
            (801396008, "KW_5", "2023-06-05", "2023-06-10", 1, "Bad customer"),
            (801396009, "KW_6", "2023-06-10", "2023-06-15", 1, "Bad customer"),
            (801396010, "KW_7", "2023-06-15", "2023-06-20", 1, "Bad customer"),
            (801396011, "KW_8", "2023-06-20", "2023-06-25", 1, "Bad customer"),
            (801396012, "KW_9", "2023-06-25", "2023-06-30", 1, "Bad customer"),
            (801396007, "KW_10", "2023-07-01", "2023-07-05", 1, "Bad customer"),
            (801396008, "KW_1", "2023-07-05", "2023-07-10", 1, "Bad customer"),
            (801396008, "KW_2", "2023-07-10", "2023-07-15", 1, "Bad customer"),
            (801396009, "KW_3", "2023-07-15", "2023-07-20", 1, "Bad customer"),
            (801396009, "KW_4", "2023-07-20", "2023-07-25", 1, "Bad customer"),
            (801396009, "KW_5", "2023-07-25", "2023-07-30", 1, "Bad customer"),
            (801396009, "KW_6", "2023-08-01", "2023-08-05", 1, "Bad customer"),
            (801396009, "KW_7", "2023-08-05", "2023-08-10", 1, "Bad customer"),
        ]

        cursor.executemany(
            "INSERT INTO KitchenwareRentals (student_id, kitchenware_id, rental_date, due_date, is_returned, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            kitchenware_rentals_data,
        )

        # Commit the transaction
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed adding test data: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


#################################
###### Data Insertion ###########
#################################

def update_db_schema():
    """Set up or update database schemas from scratch"""

    # Connect to the database provider
    setup_database()

    # Create the database schema
    connection = connect_to_database()
    cursor = connection.cursor()

    build_schema(connection, cursor)
    build_dynamic(connection, cursor)

    # Create secrets file
    secrets_file = open("secrets.txt", "w")

    # Create admin password
    admin_salt = bcrypt.gensalt()
    admin_password = bcrypt.hashpw(b'admin', admin_salt)
    secrets_file.write("admin_password = {}\n".format('admin'))

    # Create guest password
    guest_salt = bcrypt.gensalt()
    guest_password = bcrypt.hashpw(b'guest', guest_salt)
    secrets_file.write("guest_password = {}\n".format('guest'))

    try:
        # Admin has full access
        cursor.execute(
            "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
            ("admin", admin_password, 'admin'),
        )
        # Delete the user if it already exists
        cursor.execute("DROP USER IF EXISTS %s@'localhost' ", ('admin',))
        
        cursor.execute(
            "CREATE USER %s@'localhost' IDENTIFIED BY %s", ('admin', 'admin')
        )
        cursor.execute(
            "GRANT ALL PRIVILEGES ON *.* TO %s@'localhost' WITH GRANT OPTION", ('admin',)
        )

        # Guest has limited access
        cursor.execute(
            "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
            ("guest", guest_password, 'user'),
        )
        # Delete the user if it already exists
        cursor.execute("DROP USER IF EXISTS %s@'localhost' ", ('guest',))
        cursor.execute(
            "CREATE USER %s@'localhost' IDENTIFIED BY %s", ('guest', 'guest')
        )
        cursor.execute(
            "GRANT DROP, INSERT, UPDATE, DELETE, SELECT ON LulaBells.* TO %s@'localhost' WITH GRANT OPTION", ('guest',)
        )

        connection.commit()

        add_test_data(connection, cursor)

    except mysql.connector.Error as error_descriptor:
        print("Failed inserting user: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


if __name__ == "__main__":
    update_db_schema()
