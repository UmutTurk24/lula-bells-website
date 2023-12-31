import mysql.connector
import datetime


###############################
#####  Insertion Queries  #####
###############################


def insert_student(
    connection,
    cursor,
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

    try:
        cursor.execute(
            "INSERT INTO Students (student_id, student_name, student_surname, student_email, \
            class_year, residence, registration_date, notes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                student_id,
                student_name,
                student_surname,
                student_email,
                class_year,
                residence,
                registration_date,
                notes,
            ),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting student: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


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


def insert_textbooksitem(connection, cursor, book_name, owned_status=0):
    """Inserts a textbook item into the database"""

    try:
        cursor.execute(
            "INSERT INTO Textbooks (book_name, owned_status) VALUES (%s, %s)",
            (book_name, owned_status),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Textbooks item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def insert_wardrobeitem(connection, cursor, cloth_id):
    """Inserts a Wardrobe item into the database"""

    try:
        cursor.execute(
            "INSERT INTO Wardrobe (cloth_id) VALUES (%s)",
            ([cloth_id]),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Wardrobe item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def insert_wardroberental(
    connection,
    cursor,
    student_id,
    cloth_id,
    rental_date,
    due_date,
    is_returned=False,
    notes="",
):
    """Inserts a Wardrobe rental into the database"""

    try:
        cursor.execute(
            "INSERT INTO WardrobeRentals (student_id, cloth_id, rental_date, due_date, is_returned, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            (student_id, cloth_id, rental_date, due_date, is_returned, notes),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Wardrobe rental: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def insert_textbookrental(
    connection,
    cursor,
    student_id,
    book_name,
    rental_date,
    due_date,
    is_returned=False,
    notes="",
):
    """Inserts a Textbook rental into the database"""

    try:
        cursor.execute(
            "INSERT INTO TextbookRentals (student_id, book_name, rental_date, due_date, is_returned, notes) VALUES (%s, %s, %s, %s, %s, %s)",
            (student_id, book_name, rental_date, due_date, is_returned, notes),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Textbook rental: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


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


###############################
#####     Formatters      #####
###############################


def convertDate(date):
    """Converts a date string in the format YYYYMMDD to a datetime.date object"""

    year = date[0:4]
    month = date[4:6]
    day = date[6:8]

    return datetime.date(int(year), int(month), int(day))
