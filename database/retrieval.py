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

def get_all_groceries(connection):
    """Returns all groceries items in the database"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Pantry")

    result = cursor.fetchall()
    cursor.close()
    return result


def get_all_textbooks(connection):
    """Returns all textbooks items in the database"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Textbooks")

    result = cursor.fetchall()
    cursor.close()
    return result

def get_all_kitchenware(connection):
    """Returns all kitchenware items in the database"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Kitchenware")

    result = cursor.fetchall()
    cursor.close()
    return result


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

def get_all_clothes(connection):
    """Returns all clothes items in the database"""

    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Clothes")

    result = cursor.fetchall()
    cursor.close()
    return result

def get_all_textbookrentals(connection, cursor):
    """Returns all textbook rentals in the database"""
    cursor.execute("SELECT * FROM TextbookRentals")
    return cursor.fetchall()


def get_all_clothRentals(connection, cursor):
    """Returns all cloth rentals in the database"""
    cursor.execute("SELECT * FROM ClothRentals")
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


def get_kitchenwarerental_by_student(connection, student_id):
    """Returns all kitchenware rentals in the database given the student_id"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM KitchenwareRentals WHERE student_id = %s", (student_id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_possessed_textbooks_by_student(connection, student_id):
    """Returns all textbook rentals in the database given the student_id"""
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM TextbookRentals WHERE student_id = %s AND is_returned = 0",
        (student_id),
    )
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


def get_clothrental_by_student(connection, student_id):
    """Returns all cloth rentals in the database given the student_id"""
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ClothRentals WHERE student_id = %s AND is_returned = 0", (student_id,))
    result = cursor.fetchall()
    cursor.close()
    return result


def get_cloth_rental_by_clothid(connection, cursor, cloth_id):
    """Returns all cloth rentals in the database given the cloth_id"""
    cursor.execute("SELECT * FROM ClothRentals WHERE cloth_id = %s", (cloth_id,))
    return cursor.fetchall()


def get_wardroberental_by_startdate_and_enddate(
    connection, cursor, start_date, end_date
):
    """Returns all cloth rentals in the database given the start_date and end_date"""
    cursor.execute(
        "SELECT * FROM ClothRentals WHERE rental_date >= %s AND rental_date <= %s",
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

def get_textbooks_and_renters(connection):
    """Returns all textbooks and renters information in the database"""
    cursor = connection.cursor()
    cursor.execute("SELECT t.book_name, tr.rental_date, tr.is_returned FROM Textbooks as t LEFT JOIN (SELECT * FROM TextbookRentals as tr WHERE tr.is_returned = 0) as tr ON t.book_name = tr.book_name")
    result = cursor.fetchall()
    cursor.close()
    return result

def get_clothes_and_renters(connection):
    """Returns all clothes and renters information in the database"""
    cursor = connection.cursor()
    cursor.execute("SELECT w.cloth_id, wr.rental_date, wr.is_returned FROM (SELECT * FROM Clothes w) as w LEFT JOIN (SELECT * FROM ClothRentals WHERE is_returned = 0) as wr ON w.cloth_id = wr.cloth_id")
    result = cursor.fetchall()
    cursor.close()
    return result


def get_kitchenware_and_renters(connection):
    """Returns all kitchenware and renters information in the database"""
    cursor = connection.cursor()
    cursor.execute(
        "SELECT k.kitchenware_id, kr.rental_date, kr.is_returned FROM (SELECT * FROM Kitchenware k) as k LEFT JOIN (SELECT * FROM KitchenwareRentals WHERE is_returned = 0) as kr ON k.kitchenware_id = kr.kitchenware_id"
    )
    result = cursor.fetchall()
    cursor.close()
    return result


def get_grocery_items(connection):
    """Returns all groceries in the database"""
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Pantry"
    )
    result = cursor.fetchall()
    cursor.close()
    return result

def get_all_users(connection):
    """Returns all users in the database"""
    cursor = connection.cursor()
    cursor.execute(
        "SELECT * FROM Users"
    )
    result = cursor.fetchall()
    cursor.close()
    return result
