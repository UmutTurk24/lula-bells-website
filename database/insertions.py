import mysql.connector
import datetime
import bcrypt

###############################
#####  Insertion Queries  #####
###############################


def insert_student(
    connection,
    student_id,
    student_name,
    student_surname,
    student_email,
    class_year,
    residence,
    registration_date,
    notes="",
):
    """Inserts a student into the database"""

    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Students (student_id, student_name, student_surname, student_email, \
            class_year, residence, registration_date, agreement_signed, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                student_id,
                student_name,
                student_surname,
                student_email,
                class_year,
                residence,
                registration_date,
                0,
                notes,
            ),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting student: {}".format(error_descriptor))
        return None


def insert_pantryitem(connection, cursor, item_name, quantity=0, cost=0.0):
    """Inserts a pantry item into the database"""

    try:
        cursor.execute(
            "INSERT INTO Pantry (item_name, quantity, cost) VALUES (%s, %s, %s)",
            (item_name, quantity, cost),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting pantry item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def insert_grocery(connection, item_name, quantity, cost=0):
    """Inserts a grocery item into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Pantry (item_name, quantity, cost) VALUES (%s, %s, %s)",
            (item_name, quantity, cost),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting grocery item: {}".format(error_descriptor))
        return False


def insert_textbook(connection, book_name, owned_status=0):
    """Inserts a textbook item into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Textbooks (book_name, owned_status) VALUES (%s, %s)",
            (book_name, owned_status),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting textbook: {}".format(error_descriptor))
        return False


def insert_cloth(connection, cloth_id):
    """Inserts a Clothes item into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Clothes (cloth_id) VALUES (%s)",
            ([cloth_id]),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Clothes item: {}".format(error_descriptor))
        return False

def insert_kitchenware(connection, kitchenware_id):
    """Inserts a Kitchenware item into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Kitchenware (kitchenware_id) VALUES (%s)",
            ([kitchenware_id]),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Kitchenware item: {}".format(error_descriptor))
        return False

def insert_pantrypurchase(
    connection,
    cursor,
    student_id,
    item_name,
    purchase_date,
    quantity,
):
    """Inserts a Pantry rental into the database"""

    try:
        cursor.execute(
            "INSERT INTO PantryPurchase (student_id, item_name, purchase_date, quantity) VALUES (%s, %s, %s, %s)",
            (student_id, item_name, purchase_date, quantity),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Pantry rental: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)

def insert_user(connection, cursor, username, password):
    """Inserts a user into the database"""

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

        cursor.execute(
            "CREATE USER %s@'localhost' IDENTIFIED BY %s", (username, password)
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Textbooks item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)

def insert_textbook_rental(connection, student_id, textbook_name, due_date):
    """Inserts a textbook rental into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO TextbookRentals (student_id, book_name, rental_date, due_date, is_returned, notes) VALUES (%s, %s, CURDATE(), %s, 0, '')",
            (student_id, textbook_name, due_date),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting textbook rental: {}".format(error_descriptor))
        return False


def insert_cloth_rental(connection, student_id, cloth_id, due_date, renter_info =""):
    """Inserts a cloth rental into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO ClothRentals (student_id, cloth_id, rental_date, due_date, is_returned, notes, renter_info) VALUES (%s, %s, CURDATE(), %s, 0, '', %s)",
            (student_id, cloth_id, due_date, renter_info),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting kitchenware rental: {}".format(error_descriptor))
        return False


def insert_kitchenware_rental(
    connection, student_id, kitchenware_id, due_date, renter_info=""
):
    """Inserts a cloth rental into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO KitchenwareRentals (student_id, kitchenware_id, rental_date, due_date, is_returned, notes, renter_info) VALUES (%s, %s, CURDATE(), %s, 0, '', %s)",
            (student_id, kitchenware_id, due_date, renter_info),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting kitchenware rental: {}".format(error_descriptor))
        return False

def insert_pantry_purchase(connection, student_id, item_name, quantity):
    """Inserts a pantry purchase into the database"""

    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO PantryPurchase (student_id, item_name, quantity, purchase_date) VALUES (%s, %s, %s, CURDATE())",
            (student_id, item_name, quantity),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting pantry purchase: {}".format(error_descriptor))
        return False


###############################
#####     Formatters      #####
###############################


def convertDate(date):
    """Converts a date string in the format YYYYMMDD to a datetime.date object"""

    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    return datetime.date(int(year), int(month), int(day))
