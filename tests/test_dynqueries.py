from database.schema import *
from database.dyn_queries import *

#################################
######   VIEWS TESTING    #######
#################################

def test_build_view():
    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    build_test_dynamic(connection, cursor)

    cursor.close()
    connection.close()

def test_get_customer_demographics():
    connection, cursor = connect_to_test_database()
    build_test_schema(connection, cursor)
    build_test_dynamic(connection, cursor)

    # Add some data to the database
    add_test_data(connection, cursor)

    # Test the procedure
    result = get_customer_demographics(connection, cursor, '2020-01-01', '2023-12-31')
    # assert result == 1
    

