USE LulaBells;


-- Create a view that lists all students that have purchased an item from the pantry

-- Create a view that returns the number of students that have rented a textbook between two dates
-- Create a view that returns the number of students that have rented a wearable between two dates
-- Create a view that returns the number of students that have purchased an item from the pantry between two dates

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




-- PROCEDURE: Get a student's visits
CREATE PROCEDURE GetVisitsForSpecificStudent(IN given_student_id INT)
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
-- CALL GetVisitsForSpecificStudent(801396000);

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


-- VIEW: Get the students who need to return their rental clothes
CREATE VIEW OverdueWardrobeRentals AS
SELECT *
FROM WardrobeRentals wr
WHERE due_date <= CURDATE();

-- EXAMPLE SELECT * FROM OverdueWardrobeRentals;