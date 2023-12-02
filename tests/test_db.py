from database.schema import *

#################################
###### DATABASE TESTING #########
#################################


def test_connect_to_database():
    connection, cursor = connect_to_test_database()
    assert connection.is_connected() == True
    cursor.close()
    connection.close()

def test_build_schema():
    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    cursor.close()
    connection.close()

#################################
######   VIEWS TESTING    #######
#################################
