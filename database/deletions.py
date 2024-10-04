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


def delete_grocery(connection, item_name):
    """Deletes a grocery item from the database"""

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Pantry WHERE item_name = %s", (item_name,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting grocery item: {}".format(error_descriptor))
        return False

def delete_textbook(connection, book_name):
    """Deletes a textbook item from the database"""

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Textbooks WHERE book_name = %s", (book_name,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting textbook item: {}".format(error_descriptor))
        return False

def delete_cloth(connection, cloth_id):
    """Deletes a cloth item from the database"""

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Clothes WHERE cloth_id = %s", (cloth_id,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting cloth item: {}".format(error_descriptor))
        return False

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

def delete_kitchenware(connection, kitchenware_id):
    """Deletes a kitchenware item from the database"""

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Kitchenware WHERE kitchenware_id = %s", (kitchenware_id,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting kitchenware item: {}".format(error_descriptor))
        return False

def delete_cloth_rental(connection, cursor, item_name):
    """Deletes a cloth rental from the database"""

    try:
        cursor.execute("DELETE FROM ClothRentals WHERE item_name = %s", (item_name,))
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting cloth rental: {}".format(error_descriptor))
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


def delete_all_clothRentals(connection, cursor):
    """Deletes all cloth rentals from the database"""

    try:
        cursor.execute("DELETE FROM ClothRentals")
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting all cloth rentals: {}".format(error_descriptor))
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
