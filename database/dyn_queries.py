import mysql.connector


def get_visits_per_day(connection, cursor):
    """Retrieves the number of visits per day"""

    try:
        cursor.execute("SELECT * FROM VisitsPerDayView;")
        return cursor.fetchall()
    except mysql.connector.Error as error_descriptor:
        print("Failed calling the VisitsPerDayView view: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)


def get_visits_for_student(connection, student_id):
    """Retrieves the visits for the given student"""
    try:
        cursor = connection.cursor(buffered=True)
        cursor.execute("CALL GetVisitsForStudent(%s)", (student_id,))
        result = cursor.fetchall()
        cursor.close()
        # Check if the connection is alive after the procedure call
        if not connection.is_connected():
            connection.reconnect()
        return result
    except mysql.connector.Error as error_descriptor:
        print(
            "Failed calling the GetVisitsForStudent procedure: {}".format(
                error_descriptor
            )
        )
        return None


def get_customer_demographics(connection, cursor, start_date, end_date):
    """Retrieves the demographics of customers for pantry for the given date range"""

    try:
        cursor.execute("""
        SET @class_year_count_var = 0;
        SET @class_year_value_var = '';
        SET @residence_count_var = 0;
        SET @residence_value_var = '';
        SET @total_visits_var = 0;
        SET @unique_visits_var = 0;

        CALL GetCustomerDemographics(%s, %s, 
                                    @class_year_count_var, @class_year_value_var, 
                                    @residence_count_var, @residence_value_var, 
                                    @total_visits_var, @unique_visits_var);

        -- Now you can use the variables to access the results
        SELECT @class_year_count_var AS class_year_count,
            @class_year_value_var AS class_year_value,
            @residence_count_var AS residence_count,
            @residence_value_var AS residence_value,
            @total_visits_var AS total_visits,
            @unique_visits_var AS unique_visits;
        """,
            (start_date, end_date,),
        )
        return cursor.fetchall()
    except mysql.connector.Error as error_descriptor:
        print(
            "Failed calling the GetCustomerDemographics procedure: {}".format(
                error_descriptor
            )
        )
        cursor.close()
        connection.close()
        exit(1)


def get_overdue_wardrobe_rentals(connection, cursor):
    """Retrieves the overdue wardrobe rentals"""

    try:
        cursor.execute("SELECT * FROM OverdueWardrobeRentals;")
        return cursor.fetchall()
    except mysql.connector.Error as error_descriptor:
        print(
            "Failed calling the OverdueWardrobeRentals view: {}".format(
                error_descriptor
            )
        )
        cursor.close()
        connection.close()
        exit(1)


def get_overdue_textbook_rentals(connection, cursor):
    """Retrieves the overdue textbook rentals"""

    try:
        cursor.execute("SELECT * FROM OverdueTextbookRentals;")
        return cursor.fetchall()
    except mysql.connector.Error as error_descriptor:
        print(
            "Failed calling the OverdueTextbookRentals view: {}".format(
                error_descriptor
            )
        )
        cursor.close()
        connection.close()
        exit(1)
