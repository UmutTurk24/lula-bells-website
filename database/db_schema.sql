DROP SCHEMA IF EXISTS LulaBells;
CREATE SCHEMA LulaBells;
USE LulaBells;

CREATE TABLE Students
	(student_id				INTEGER(9) CHECK(LENGTH(student_id) = 9),
	 student_name			VARCHAR(40),
	 student_surname		VARCHAR(40),
	 student_email			VARCHAR(100),
	 class_year				INTEGER,
	 residence				BOOLEAN,
	 registration_date		DATE,
	 agreement_signed		BOOLEAN,
	 notes 					VARCHAR(500),
	 PRIMARY KEY (student_id)
	);

CREATE TABLE Textbooks
	(book_name				VARCHAR(200),
	owned_status			BOOLEAN,
	PRIMARY KEY (book_name)
	);

CREATE TABLE TextbookRentals
	(student_id 			INTEGER(9),
	book_name				VARCHAR(200),
	rental_date				DATE,
	due_date				DATE,
	is_returned				BOOLEAN,
	notes 					VARCHAR(500),
	FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (book_name) REFERENCES Textbooks (book_name) ON DELETE CASCADE ON UPDATE CASCADE
	);

CREATE TABLE Clothes
	(cloth_id				VARCHAR(100),
	PRIMARY KEY (cloth_id)
	);

CREATE TABLE ClothRentals
	(student_id 			INTEGER(9),
	cloth_id				VARCHAR(100),
	rental_date				DATE,
	due_date				DATE,
	is_returned				BOOLEAN,
	notes 					VARCHAR(1000),
	renter_info				VARCHAR(75),
	FOREIGN KEY (cloth_id) REFERENCES Clothes (cloth_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE ON UPDATE CASCADE
	);

CREATE TABLE Pantry
	(item_name				VARCHAR(100),
	quantity				INT,
	cost 					DECIMAL(6,2),
	PRIMARY KEY (item_name)
	);

CREATE TABLE PantryPurchase
	(student_id 			INTEGER(9),
	item_name				VARCHAR(100),
	quantity				INT,
	purchase_date			DATE,
	FOREIGN KEY (item_name) REFERENCES Pantry (item_name) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE ON UPDATE CASCADE
	);


CREATE TABLE Kitchenware
	(kitchenware_id				VARCHAR(100),
	PRIMARY KEY (kitchenware_id)
	);

CREATE TABLE KitchenwareRentals
	(student_id 			INTEGER(9),
	kitchenware_id			VARCHAR(100),
	rental_date				DATE,
	due_date				DATE,
	is_returned				BOOLEAN,
	notes 					VARCHAR(1000),
	renter_info				VARCHAR(75),
	FOREIGN KEY (kitchenware_id) REFERENCES Kitchenware (kitchenware_id) ON DELETE CASCADE ON UPDATE CASCADE,
	FOREIGN KEY (student_id) REFERENCES Students (student_id) ON DELETE CASCADE ON UPDATE CASCADE
	);

CREATE TABLE Users
	(user_id				INT NOT NULL AUTO_INCREMENT,
	username				VARCHAR(50),
	password				VARCHAR(128),
	role 					VARCHAR(20),
	PRIMARY KEY (user_id)
);
