import os
from flask_login import LoginManager
import flask_login

import mysql.connector
from database.schema import connect_to_database

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")


class User(flask_login.UserMixin):
    def __init__(self, id, username, password, role):
        self.id = id
        self.username = username
        self.password = password
        self.role = role


# Function to get user by ID
def get_user_by_id(user_id):
    mydb = connect_to_database()
    cursor = mydb.cursor()

    cursor.execute("SELECT * FROM Users WHERE user_id = %s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    print(user)
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None


# Function to get user by username
def get_user_by_username(connection, username):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user[0], user[1], user[2], user[3])
    return None


# Function to create a new user
def create_user(connection, username, password, role):
    try: 
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO Users (username, password, role) VALUES (%s, %s, %s)",
            (username, password, role),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting Clothes item: {}".format(error_descriptor))
        return False

# Function to change user password
def change_password(connection, username, password):
    try:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE Users SET password = %s WHERE username = %s",
            (password, username),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating password: {}".format(error_descriptor))
        return False

# Function to delete a user
def delete_user(connection, username):
    try:
        cursor = connection.cursor()

        cursor.execute("DELETE FROM Users WHERE username = %s", (username,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting user: {}".format(error_descriptor))


# Function to change user role
def update_user_role(connection, username, role):
    try:
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE Users SET role = %s WHERE username = %s",
            (role, username),
        )
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed updating role: {}".format(error_descriptor))
        return False
