from database.insertions import *


###############################
###### Delete One Item  #######
###############################


def delete_student(connection, cursor, student_id):
    """Deletes a student from the database"""

    try:
        cursor.execute("DELETE FROM Students WHERE student_id = %s", (student_id,))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting student: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_pantryitem(connection, cursor, item_name):
    """Deletes a pantry item from the database"""

    try:
        cursor.execute("DELETE FROM Pantry WHERE item_name = %s", (item_name,))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting pantry item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_textbookitem(connection, cursor, book_name):
    """Deletes a textbook item from the database"""

    try:
        cursor.execute("DELETE FROM Textbooks WHERE book_name = %s", (book_name,))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting textbook item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_textbookrental(connection, cursor, book_name):
    """Deletes a textbook rental from the database"""

    try:
        cursor.execute("DELETE FROM TextbookRentals WHERE book_name = %s", (book_name,))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting textbook rental: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_wardroberental(connection, cursor, item_name):
    """Deletes a wardrobe rental from the database"""

    try:
        cursor.execute("DELETE FROM WardrobeRentals WHERE item_name = %s", (item_name,))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting wardrobe rental: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)

###############################
######  Delete Groups   #######
###############################

def delete_all_students(connection, cursor):
    """Deletes all students from the database"""

    try:
        cursor.execute("DELETE FROM Students")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all students: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_all_pantryitems(connection, cursor):
    """Deletes all Pantry items from the database"""

    try:
        cursor.execute("DELETE FROM Pantry")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all Pantry items: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_all_textbookitems(connection, cursor):
    """Deletes all textbook items from the database"""

    try:
        cursor.execute("DELETE FROM Textbooks")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all textbook items: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_all_pantrypurchases(connection, cursor):
    """Deletes all pantry purchases from the database"""

    try:
        cursor.execute("DELETE FROM PantryPurchases")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all pantry purchases: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_all_textbookrentals(connection, cursor):
    """Deletes all textbook rentals from the database"""

    try:
        cursor.execute("DELETE FROM TextbookRentals")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all textbook rentals: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def delete_all_wardroberentals(connection, cursor):
    """Deletes all wardrobe rentals from the database"""

    try:
        cursor.execute("DELETE FROM WardrobeRentals")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all wardrobe rentals: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


###############################
######    Delete All    #######
###############################


def delete_all(connection, cursor):
    """Deletes all items from the database"""

    try:
        cursor.execute("DELETE FROM Students")
        cursor.execute("DELETE FROM Pantry")
        cursor.execute("DELETE FROM Textbooks")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all items: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)
