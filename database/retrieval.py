def get_all_students(connection, cursor):
    """Returns all students in the database"""
    cursor.execute("SELECT * FROM students")
    return cursor.fetchall()


def get_students_for_search_bar(connection):
    """Returns name, last name, and id of students in the database"""
    cursor = connection.cursor()
    cursor.execute("SELECT student_id, student_name, student_surname FROM students")
    result = cursor.fetchall()
    cursor.close()
    return result


def get_all_pantry(connection, cursor):
    """Returns all pantry items in the database"""
    cursor.execute("SELECT * FROM Pantry")
    return cursor.fetchall()


def get_all_textbooks(connection, cursor):
    """Returns all textbooks items in the database"""
    cursor.execute("SELECT * FROM Textbooks")
    return cursor.fetchall()


def get_student(connection, student_id):
    """Returns a student in the database given the student_id"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Students WHERE student_id = %s", (student_id,))
    result = cursor.fetchone()
    cursor.close()
    return result


def get_pantryitem(connection, cursor, item_name):
    """Returns a pantry item in the database given the item_name"""
    cursor.execute("SELECT * FROM Pantry WHERE item_name = %s", (item_name,))
    return cursor.fetchone()


def get_textbookitem(connection, cursor, book_name):
    """Returns a textbook item in the database given the book_name"""
    cursor.execute("SELECT * FROM Textbooks WHERE book_name = %s", (book_name,))
    return cursor.fetchone()


def get_all_textbookrentals(connection, cursor):
    """Returns all textbook rentals in the database"""
    cursor.execute("SELECT * FROM TextbookRentals")
    return cursor.fetchall()


def get_all_wardroberentals(connection, cursor):
    """Returns all wardrobe rentals in the database"""
    cursor.execute("SELECT * FROM WardrobeRentals")
    return cursor.fetchall()


def get_all_pantrypurchases(connection, cursor):
    """Returns all pantry purchases in the database"""
    cursor.execute("SELECT * FROM PantryPurchase")
    return cursor.fetchall()


def get_textbookrental_by_student(connection, student_id):
    """Returns all textbook rentals in the database given the student_id"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM TextbookRentals WHERE student_id = %s", (student_id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_textbookrental_by_bookname(connection, cursor, book_name):
    """Returns all textbook rentals in the database given the book_name"""
    cursor.execute("SELECT * FROM TextbookRentals WHERE book_name = %s", (book_name,))
    return cursor.fetchall()


def get_textbookrental_by_startdate_and_enddate(
    connection, cursor, start_date, end_date
):
    """Returns all textbook rentals in the database given the start_date and end_date"""
    cursor.execute(
        "SELECT * FROM TextbookRentals WHERE rental_date >= %s AND rental_date <= %s",
        (start_date, end_date),
    )
    return cursor.fetchall()


def get_wardroberental_by_student(connection, student_id):
    """Returns all wardrobe rentals in the database given the student_id"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM WardrobeRentals WHERE student_id = %s", (student_id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_wardroberental_by_clothid(connection, cursor, cloth_id):
    """Returns all wardrobe rentals in the database given the cloth_id"""
    cursor.execute("SELECT * FROM WardrobeRentals WHERE cloth_id = %s", (cloth_id,))
    return cursor.fetchall()


def get_wardroberental_by_startdate_and_enddate(
    connection, cursor, start_date, end_date
):
    """Returns all wardrobe rentals in the database given the start_date and end_date"""
    cursor.execute(
        "SELECT * FROM WardrobeRentals WHERE rental_date >= %s AND rental_date <= %s",
        (start_date, end_date),
    )
    return cursor.fetchall()


def get_pantrypurchase_by_student(connection, cursor, student_id):
    """Returns all pantry purchases in the database given the student_id"""
    cursor.execute("SELECT * FROM PantryPurchase WHERE student_id = %s", (student_id,))
    return cursor.fetchall()

def get_pantrypurchase_by_itemname(connection, cursor, item_name):
    """Returns all pantry purchases in the database given the item_name"""
    cursor.execute("SELECT * FROM PantryPurchase WHERE item_name = %s", (item_name,))
    return cursor.fetchall()


def get_pantrypurchase_by_startdate(connection, cursor, start_date):
    """Returns all pantry purchases in the database given the start_date"""
    cursor.execute(
        "SELECT * FROM PantryPurchase WHERE purchase_date >= %s", (start_date,)
    )
    return cursor.fetchall()


def get_pantry_purchase_by_startdate_and_enddate(
    connection, cursor, start_date, end_date
):
    """Returns all pantry purchases in the database given the start_date and end_date"""
    cursor.execute(
        "SELECT * FROM PantryPurchase WHERE purchase_date >= %s AND purchase_date <= %s",
        (start_date, end_date),
    )
    return cursor.fetchall()
