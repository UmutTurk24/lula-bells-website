USE TestLulaBells;

-- Demographics Report class year, residence, and total amount of visits + uniqueness
-- Visit counts by date
-- Allow only 4 class years on the website. ex: 2020, 2021, 2022, 2023
-- at the end of the each year, do the summer start and summer end button
-- at the end of each semester, do the registration pop up.

-- Tickbox late stuff

-- VIEW: Get number of visits each day	
CREATE VIEW VisitsPerDayView AS
SELECT t.purchase_date, SUM(num_visits) AS total_visits
FROM (
    SELECT DISTINCT purchase_date, COUNT(*) as num_visits
    FROM PantryPurchase pp
    GROUP BY student_id, purchase_date
) AS t
GROUP BY t.purchase_date;
-- Example: SELECT * FROM VisitsPerDayView;

-- PROCEDURE: Get number of visits each day for a specific student
CREATE PROCEDURE GetVisitsForStudent(IN given_student_id INT)
BEGIN
    SELECT *
    FROM (
        SELECT *
        FROM Students s
        WHERE s.student_id = given_student_id
    ) AS st
    JOIN (
        SELECT student_id
        FROM PantryPurchase pp
        GROUP BY student_id, purchase_date
    ) AS pr ON pr.student_id = st.student_id;
END;
-- Example usage: CALL GetVisitsForStudent(801396000);

-- Get the number of visits each day between two days
CREATE PROCEDURE GetVisitsBetweenDates(IN start_date DATE, IN end_date DATE)
BEGIN
    SELECT t.purchase_date, SUM(num_visits)
    FROM (
        SELECT DISTINCT purchase_date, COUNT(*) AS num_visits
        FROM PantryPurchase pp
        WHERE pp.purchase_date BETWEEN start_date AND end_date
        GROUP BY student_id, purchase_date
    ) AS t
    GROUP BY t.purchase_date;
END;
-- Example usage: CALL GetVisitsBetweenDates('2019-01-01', '2019-12-31');

-- PROCEDURE: Get the demographics of the customers
CREATE PROCEDURE GetCustomerDemographics(
    IN start_date DATE,
    IN end_date DATE,
    OUT class_year_count INT,
    OUT class_year_value VARCHAR(255),
    OUT residence_count INT,
    OUT residence_value VARCHAR(255),
    OUT total_visits INT,
    OUT unique_visits INT
)
BEGIN
    -- Get the class year from demographics
    SELECT COUNT(s.class_year), s.class_year
    INTO class_year_count, class_year_value
    FROM (
        SELECT student_id, purchase_date
        FROM PantryPurchase
        WHERE purchase_date BETWEEN start_date AND end_date
        GROUP BY student_id, purchase_date
    ) AS pp
    JOIN Students s ON s.student_id = pp.student_id
    GROUP BY s.class_year;

    -- Get the residence
    SELECT COUNT(s.residence), s.residence
    INTO residence_count, residence_value
    FROM (
        SELECT student_id, purchase_date
        FROM PantryPurchase
        WHERE purchase_date BETWEEN start_date AND end_date
        GROUP BY student_id, purchase_date
    ) AS pp
    JOIN Students s ON s.student_id = pp.student_id
    GROUP BY s.residence;

    -- Get the total visit
    SELECT COUNT(*) INTO total_visits
    FROM (
        SELECT student_id, purchase_date
        FROM PantryPurchase
        WHERE purchase_date BETWEEN start_date AND end_date
        GROUP BY student_id, purchase_date
    ) AS f;

    -- Get the total unique visits
    SELECT COUNT(DISTINCT student_id) INTO unique_visits
    FROM (
        SELECT student_id, purchase_date
        FROM PantryPurchase
        WHERE purchase_date BETWEEN start_date AND end_date
        GROUP BY student_id, purchase_date
    ) AS f;
    
    -- Return the results
    SELECT class_year_count, class_year_value, residence_count, residence_value, total_visits, unique_visits;
END;


/* 
Example Usage:

-- Declare variables to store the results
SET @class_year_count_var = 0;
SET @class_year_value_var = '';
SET @residence_count_var = 0;
SET @residence_value_var = '';
SET @total_visits_var = 0;
SET @unique_visits_var = 0;

-- Call the procedure with specific start_date and end_date
CALL GetCustomerDemographics('2023-01-01', '2023-12-31', 
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
 */

-- VIEW: Get the students who need to return their rental clothes
CREATE VIEW OverdueWardrobeRentals AS
SELECT *
FROM WardrobeRentals wr
WHERE due_date <= CURDATE();
-- EXAMPLE SELECT * FROM OverdueWardrobeRentals;

-- VIEW: Get the students who need to return their rental clothes
CREATE VIEW OverdueTextbookRentals AS
SELECT *
FROM TextbookRentals tr
WHERE is_returned = FALSE;
-- EXAMPLE SELECT * FROM OverdueTextbookRentals;



