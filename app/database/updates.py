import mysql.connector

###############################
###### Update One Item  #######
###############################


def update_student(
    connection,
    cursor,
    student_id,
    student_name,
    student_surname,
    student_email,
    class_year,
    residence,
    registration_date,
    notes,
):
    """Updates a student in the database given the student_id"""

    try:
        cursor.execute(
            "UPDATE Students SET student_name = %s, student_surname = %s, student_email = %s, class_year = %s, \
            residence = %s, registration_date = %s, notes = %s WHERE student_id = %s",
            (
                student_name,
                student_surname,
                student_email,
                class_year,
                residence,
                registration_date,
                notes,
                student_id,
            ),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed updating student: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)

def update_grocery(connection, item_name, quantity, cost):
    """Updates a grocery item in the database given the item_name"""

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Pantry SET quantity = %s, cost = %s WHERE item_name = %s",
            (quantity, cost, item_name),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating grocery item: {}".format(error_descriptor))
        return None

def update_textbookitem(connection, cursor, old_book_name, owned_status, new_book_name):
    """Updates a textbook item in the database given the book_name"""

    try:
        cursor.execute(
            "UPDATE Textbooks SET book_name = %s, owned_status = %s WHERE book_name = %s",
            (new_book_name, owned_status, old_book_name),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed updating textbook item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def update_pantry_purchase(connection, quantity, purchase_date, student_id, item_name):
    """Updates a grocery visit item in the database given the visit_id"""

    print(quantity, purchase_date, student_id, item_name)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE PantryPurchase SET quantity = %s WHERE purchase_date = %s AND student_id = %s AND item_name = %s",
            (quantity, purchase_date, student_id, item_name),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating grocery visit item: {}".format(error_descriptor))
        return None


def update_rented_cloth(connection, due_date, student_id, cloth_id, is_returned):
    """Updates a rented clothing item in the database"""

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE ClothRentals SET is_returned = %s WHERE student_id = %s AND cloth_id = %s AND due_date = %s",
            (is_returned, student_id, cloth_id, due_date),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating rented clothing: {}".format(error_descriptor))
        return None


def update_rented_textbook(
    connection, due_date, student_id, textbook_name, is_returned
):
    """Updates a rented textbook item in the database"""
    print(due_date, student_id, textbook_name, is_returned)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE TextbookRentals SET is_returned = %s WHERE student_id = %s AND book_name = %s AND due_date = %s",
            (is_returned, student_id, textbook_name, due_date),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating rented texbtook: {}".format(error_descriptor))
        return None


def update_rented_kitchenware(
    connection, due_date, student_id, kitchenware_name, is_returned
):
    """Updates a rented textbook item in the database"""
    print(due_date, student_id, kitchenware_name, is_returned)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE KitchenwareRentals SET is_returned = %s WHERE student_id = %s AND kitchenware_id = %s AND due_date = %s",
            (is_returned, student_id, kitchenware_name, due_date),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating rented kitchenware: {}".format(error_descriptor))
        return None


def student_agreement(connection, student_id, agreement_signed):
    """Updates a student agreement in the database given the student_id"""

    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE Students SET agreement_signed = %s WHERE student_id = %s",
            (agreement_signed, student_id),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating student agreement: {}".format(error_descriptor))
        return None
