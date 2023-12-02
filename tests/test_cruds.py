from database.insertions import *
from database.schema import *
from database.retrieval import *
from database.deletions import *
from database.updates import *
from database.retrieval import *


#################################
###### INSERTION TESTING ########
#################################
def test_populate_students():
    """Tests that students can be inserted into the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(9):
        insert_student(
            connection,
            cursor,
            "80139601" + str(index),
            "student_name",
            "student_surname",
            "umo@davidson.edu",
            2024,
            1,
            convertDate("20200220"),
            "This is a student"
        )
    results = get_all_students(connection, cursor)
    assert len(results) == 9
    cursor.close()
    connection.close()


def test_populate_pantry():
    """Tests that pantry items can be inserted into the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(100):
        insert_pantryitem(connection, cursor, "item_name" + str(index), 0)
    results = get_all_pantry(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()


def test_populate_textbooks():
    """Tests that textbook items can be inserted into the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(100):
        insert_textbooksitem(connection, cursor, "book_name" + str(index), 0)
    results = get_all_textbooks(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()


def test_populate_textbookrental():
    """Tests that textbook rentals can be inserted into the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)

    # Insert textbooks
    for index in range(10):
        insert_textbooksitem(connection, cursor, "book_name" + str(index), 0)

    # Insert a student
    for index in range(10):
        insert_student(
            connection,
            cursor,
            "80139601" + str(index),
            "student_name",
            "student_surname",
            "umo@davidson.edu",
            2024,
            1,
            convertDate("20200220"),
            "This is a student in need",
        )

    for index in range(10):
        insert_textbookrental(
            connection,
            cursor,
            "80139601" + str(index),
            "book_name" + str(index),
            convertDate("20200220"),
            convertDate("20200220"),
            False,
        )
    results = get_all_textbookrentals(connection, cursor)
    assert len(results) == 10
    cursor.close()
    connection.close()


#################################
###### DELETION TESTING #########
#################################


def test_delete_student():
    """Tests that a student can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
        "This is a cool student",
    )
    delete_student(connection, cursor, "801396010")
    results = get_all_students(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


def test_delete_pantryitem():
    """Tests that a pantry item can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_pantryitem(connection, cursor, "item_name", 0)
    delete_pantryitem(connection, cursor, "item_name")
    results = get_all_pantry(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


def test_delete_textbookitem():
    """Tests that a textbook item can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_textbooksitem(connection, cursor, "book_name", 0)
    delete_textbookitem(connection, cursor, "book_name")
    results = get_all_textbooks(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


def test_delete_all_students():
    """Tests that all students can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(9):
        insert_student(
            connection,
            cursor,
            "80139601" + str(index),
            "student_name",
            "student_surname",
            "umo@davidson.edu",
            2024,
            1,
            convertDate("20200220"),
            "Cool students",
        )
    delete_all_students(connection, cursor)
    results = get_all_students(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


def test_delete_all_pantryitems():
    """Tests that all pantry items can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(100):
        insert_pantryitem(connection, cursor, "item_name" + str(index), 0)
    delete_all_pantryitems(connection, cursor)
    results = get_all_pantry(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


def test_delete_all_textbookitems():
    """Tests that all textbook items can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(100):
        insert_textbooksitem(connection, cursor, "book_name" + str(index), 0)
    delete_all_textbookitems(connection, cursor)
    results = get_all_textbooks(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


def test_delete_all_textbookrentals():
    """Tests that all textbook rentals can be deleted from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a textbook

    insert_textbooksitem(connection, cursor, "book_name", 0)

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
        "Naur",
    )

    # Insert textbook rentals
    for index in range(100):
        insert_textbookrental(
            connection,
            cursor,
            "801396010",
            "book_name",
            convertDate("20200220"),
            convertDate("20200221"),
            False,
            "cool note",
        )
    delete_all_textbookrentals(connection, cursor)
    results = get_all_textbookrentals(connection, cursor)
    assert len(results) == 0
    cursor.close()
    connection.close()


#################################
######   UPDATE TESTING   #######
#################################


def test_update_student():
    """Tests that a student can be updated in the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
        "This is a cool student",
    )

    update_student(
        connection,
        cursor,
        "801396010",
        "new_name",
        "new_surname",
        "new_email",
        2024,
        0,
        convertDate("20200220"),
        "This is a cool student",
    )
    results = get_all_students(connection, cursor)

    # Check that the student name and surname have been updated
    assert results[0][1] == "new_name"
    assert results[0][2] == "new_surname"
    cursor.close()
    connection.close()


def test_update_pantryitem():
    """Tests that a pantry item can be updated in the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_pantryitem(connection, cursor, "item_name", 0, 0.5)

    update_pantryitem(connection, cursor, "item_name", 1, 0.1)
    results = get_all_pantry(connection, cursor)

    # Check that the pantry item stock has been updated
    assert results[0][1] == 1
    cursor.close()
    connection.close()


def test_update_textbookitem():
    """Tests that a textbook item can be updated in the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_textbooksitem(connection, cursor, "book_name", 0)

    update_textbookitem(connection, cursor, "book_name", 0, "new_book_name")
    results = get_all_textbooks(connection, cursor)

    # Check that the textbook item stock has been updated
    assert results[0][0] == "new_book_name"  # Or False
    cursor.close()
    connection.close()


#################################
######  RETRIEVAL TESTING #######
#################################


def test_get_student():
    """Tests that a student can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        0,
        convertDate("20200220"),
        "This is a cool student",
    )
    results = get_student(connection, cursor, "801396010")
    assert results[0] == 801396010
    assert results[1] == "student_name"
    assert results[2] == "student_surname"
    assert results[3] == "umo@davidson.edu"
    assert results[4] == 2024
    assert results[5] == 0
    assert results[6] == convertDate("20200220")
    assert results[7] == "This is a cool student"
    cursor.close()
    connection.close()


def test_get_pantryitem():
    """Tests that a pantry item can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_pantryitem(connection, cursor, "item_name", 0)
    results = get_pantryitem(connection, cursor, "item_name")
    assert results[0] == "item_name"
    assert results[1] == 0
    assert results[2] == 0
    cursor.close()
    connection.close()


def test_get_textbookitem():
    """Tests that a textbook item can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    insert_textbooksitem(connection, cursor, "book_name", 0)
    results = get_textbookitem(connection, cursor, "book_name")
    assert results[0] == "book_name"
    assert results[1] == 0
    cursor.close()
    connection.close()


def test_get_textbookrental():
    """Tests that a textbook rental can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a textbook

    insert_textbooksitem(connection, cursor, "book_name")

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
        "This is a student",
    )

    # Insert textbook rentals
    insert_textbookrental(
        connection,
        cursor,
        "801396010",
        "book_name",
        convertDate("20200220"),
        convertDate("20200221"),
        False,
    )
    results = get_textbookrental_by_bookname(connection, cursor, "book_name")
    assert results[0][0] == 801396010
    assert results[0][1] == "book_name"
    assert results[0][2] == convertDate("20200220")
    assert results[0][3] == convertDate("20200221")
    assert results[0][4] == 0  # Or False

    results = get_textbookrental_by_student(connection, cursor, "801396010")
    assert results[0][0] == 801396010
    assert results[0][1] == "book_name"
    assert results[0][2] == convertDate("20200220")
    assert results[0][3] == convertDate("20200221")
    assert results[0][4] == 0  # Or False

    results = get_textbookrental_by_startdate_and_enddate(
        connection, cursor, convertDate("20200220"), convertDate("20200221")
    )
    assert results[0][0] == 801396010
    assert results[0][1] == "book_name"
    assert results[0][2] == convertDate("20200220")
    assert results[0][3] == convertDate("20200221")
    assert results[0][4] == 0  # Or False

    cursor.close()
    connection.close()


def test_get_wardroberental():
    """Tests that a wardrobe rental can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a wardrobe item

    insert_wardrobeitem(connection, cursor, "cloth_id")

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
        "This is a student",
    )

    # Insert wardrobe rentals
    insert_wardroberental(
        connection,
        cursor,
        "801396010",
        "cloth_id",
        convertDate("20200220"),
        convertDate("20200221"),
        False,
        "Some note",
    )
    results = get_wardroberental_by_student(connection, cursor, "801396010")
    assert results[0][0] == 801396010
    assert results[0][1] == "cloth_id"
    assert results[0][2] == convertDate("20200220")
    assert results[0][3] == convertDate("20200221")
    assert results[0][4] == 0  # Or False
    assert results[0][5] == "Some note"

    results = get_wardroberental_by_clothid(connection, cursor, "cloth_id")
    assert results[0][0] == 801396010
    assert results[0][1] == "cloth_id"
    assert results[0][2] == convertDate("20200220")
    assert results[0][3] == convertDate("20200221")
    assert results[0][4] == 0  # Or False
    assert results[0][5] == "Some note"

    results = get_wardroberental_by_startdate_and_enddate(
        connection, cursor, convertDate("20200220"), convertDate("20200221")
    )
    assert results[0][0] == 801396010
    assert results[0][1] == "cloth_id"
    assert results[0][2] == convertDate("20200220")
    assert results[0][3] == convertDate("20200221")
    assert results[0][4] == 0  # Or False
    assert results[0][5] == "Some note"

    cursor.close()
    connection.close()


def test_get_pantrypurchase():
    """Tests that a pantry purchase can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a pantry item

    insert_pantryitem(connection, cursor, "item_name", 0)

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
    )

    # Insert pantry purchases
    insert_pantrypurchase(
        connection,
        cursor,
        "801396010",
        "item_name",
        convertDate("20200220"),
        1,
    )

    results = get_pantrypurchase_by_student(connection, cursor, "801396010")
    assert results[0][0] == 801396010
    assert results[0][1] == "item_name"
    assert results[0][2] == 1
    assert results[0][3] == convertDate("20200220")

    results = get_pantrypurchase_by_itemname(connection, cursor, "item_name")
    assert results[0][0] == 801396010
    assert results[0][1] == "item_name"
    assert results[0][2] == 1
    assert results[0][3] == convertDate("20200220")

    results = get_pantrypurchase_by_startdate(
        connection, cursor, convertDate("20200220")
    )
    assert results[0][0] == 801396010
    assert results[0][1] == "item_name"
    assert results[0][2] == 1
    assert results[0][3] == convertDate("20200220")

    results = get_pantry_purchase_by_startdate_and_enddate(
        connection, cursor, convertDate("20200220"), convertDate("20200221")
    )
    assert results[0][0] == 801396010
    assert results[0][1] == "item_name"
    assert results[0][2] == 1
    assert results[0][3] == convertDate("20200220")

    cursor.close()
    connection.close()


def test_get_all_students():
    """Tests that all students can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(9):
        insert_student(
            connection,
            cursor,
            "80139601" + str(index),
            "student_name",
            "student_surname",
            "umo@davidson.edu",
            2024,
            0,
            convertDate("20200220"),
        )
    results = get_all_students(connection, cursor)
    assert len(results) == 9
    cursor.close()
    connection.close()


def test_get_all_pantry():
    """Tests that all pantry items can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(100):
        insert_pantryitem(connection, cursor, "item_name" + str(index), 0)
    results = get_all_pantry(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()


def test_get_all_textbooks():
    """Tests that all textbook items can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    for index in range(100):
        insert_textbooksitem(connection, cursor, "book_name" + str(index))
    results = get_all_textbooks(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()


def test_get_all_textbookrentals():
    """Tests that all textbook rentals can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a textbook

    insert_textbooksitem(connection, cursor, "book_name")

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
    )

    # Insert textbook rentals
    for index in range(100):
        insert_textbookrental(
            connection,
            cursor,
            "801396010",
            "book_name",
            convertDate("20200220"),
            convertDate("20200221"),
            False,
        )
    results = get_all_textbookrentals(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()


def test_get_all_wardroberentals():
    """Tests that all wardrobe rentals can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a wardrobe item

    insert_wardrobeitem(connection, cursor, "cloth_id")

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
    )

    # Insert wardrobe rentals
    for index in range(100):
        insert_wardroberental(
            connection,
            cursor,
            "801396010",
            "cloth_id",
            convertDate("20200220"),
            convertDate("20200221"),
            False,
        )
    results = get_all_wardroberentals(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()


def test_get_all_pantrypurchases():
    """Tests that all pantry purchases can be retrieved from the database"""

    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    # Insert a pantry item

    insert_pantryitem(connection, cursor, "item_name", 0)

    # Insert a student
    insert_student(
        connection,
        cursor,
        "801396010",
        "student_name",
        "student_surname",
        "umo@davidson.edu",
        2024,
        1,
        convertDate("20200220"),
    )

    # Insert pantry purchases
    for index in range(100):
        insert_pantrypurchase(
            connection,
            cursor,
            "801396010",
            "item_name",
            convertDate("20200220"),
            1,
        )
    results = get_all_pantrypurchases(connection, cursor)
    assert len(results) == 100
    cursor.close()
    connection.close()
