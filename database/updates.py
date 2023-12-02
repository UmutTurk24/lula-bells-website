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


def update_pantryitem(connection, cursor, item_name, quantity, cost):
    """Updates a pantry item in the database given the item_name"""

    try:
        cursor.execute(
            "UPDATE Pantry SET quantity = %s, cost = %s WHERE item_name = %s",
            (quantity, cost, item_name),
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed updating pantry item: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


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
