USE LulaBells;

-- Create a view that lists all students that have rented a textbook
-- Create a view that lists all students that have rented a wearable
-- Create a view that lists all students that have purchased an item from the pantry

-- Create a view that returns the number of students that have rented a textbook between two dates
-- Create a view that returns the number of students that have rented a wearable between two dates
-- Create a view that returns the number of students that have purchased an item from the pantry between two dates

-- Create a view that returns all the pantry purchases made by a student grouped by date
-- Create a view that returns all the textbook rentals made by a student in a semester

-- Create a view that lists all students that has late textbook rentals
-- Create a view that lists all students that has textbook rentals that are due on a given date
-- Create a view that lists all students that has textbook rentals that are due after the given date

-- Ability to track grocery visits *and* items/inventory - similar to PantrySoft
-- More important to be able to report out on the food/hygiene items that have LEFT the space than it is to have an ongoing inventory where we input orders too.

-- Lula Bell's staff needs to be able to update/edit the site as needed

-- USE TennisSchema;

-- DROP FUNCTION IF EXISTS aceCount;
-- DROP PROCEDURE IF EXISTS showAggregateStatistics;
-- DROP VIEW IF EXISTS TopAces;
-- DROP TRIGGER IF EXISTS onInsertionPlayer;

-- -- Calculates the average number of aces, given a player name and a time frame between two dates.
-- -- The function returns the average number of aces as an integer
-- -- Given multiple players, returns the first one from the dataset
-- CREATE FUNCTION aceCount (player_name_given VARCHAR(50), start_d DATE, finish_d DATE) RETURNS INT READS SQL DATA
-- BEGIN
--     DECLARE ace_average INT;

--     SELECT AVG(ace) AS avg_aces INTO ace_average
--     FROM Plays
--     WHERE player_id IN (SELECT player_id FROM Players WHERE player_name_given = player_name)
--     AND match_id IN (SELECT match_id FROM Matches WHERE t_id IN (SELECT t_id FROM Tournaments WHERE t_date BETWEEN start_d AND finish_d))
--     GROUP BY player_id LIMIT 1;

--     RETURN ace_average;
-- END;



-- -- Yields a result set containing all aggregate statistics of a player during a specific time frame
-- -- Statistics are: player_rank, ace, df, svpt, first_in, first_won, second_won
-- -- Find the average of all these statistics for a player during a specific time frame
-- -- NULL Variables are not included in the average calculation
-- CREATE PROCEDURE showAggregateStatistics (IN player_name_given VARCHAR(50), IN start_d DATE, IN finish_d DATE)
-- BEGIN
--     SELECT AVG(player_rank) AS player_rank, AVG(ace) AS ace, AVG(df) AS df, AVG(svpt) AS svpt, AVG(first_in) AS first_in, AVG(first_won) AS first_won, AVG(second_won) AS second_won
--     FROM Plays
--     WHERE player_id IN (SELECT player_id FROM Players WHERE player_name_given = player_name)
--     AND match_id IN (SELECT match_id FROM Matches WHERE t_id IN (SELECT t_id FROM Tournaments WHERE t_date BETWEEN start_d AND finish_d))
--     GROUP BY player_id;
-- END;

-- -- A view TopAces that lists the top 10 players based on number of aces, across all matches.
-- -- We have chosen to do INNER JOIN to combine the tables, because we want to get all the players
-- -- that has played at least one match
-- CREATE VIEW TopAces AS
-- SELECT player_name, ace
-- FROM Players
-- INNER JOIN Plays ON Players.player_id = Plays.player_id
-- ORDER BY ace DESC
-- LIMIT 10;

-- -- A trigger onInsertionPlayer that, upon inserting players, replaces a reference to the country code ’RUS’
-- -- (and another former country of the block, say ’EST’) to ’USR’, for the former USSR.
-- CREATE TRIGGER onInsertionPlayer BEFORE INSERT ON Players
-- FOR EACH ROW
-- BEGIN
--     IF NEW.ioc = 'RUS' THEN
--         SET NEW.ioc = 'USR';
--     END IF;
--     IF NEW.ioc = 'BRA' THEN
--         SET NEW.ioc = 'TUR';
--     END IF;
-- END;
