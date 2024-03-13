from schema import (
    build_schema,
    build_dynamic,
    create_database,
    connect_to_database,
    connect_to_database_provider,
)

from insertions import insert_user
import bcrypt
import mysql.connector


def setup_database():
    """Set up the database from scratch"""

    connection, cursor = connect_to_database_provider()

    create_database(cursor)

    cursor.close()
    connection.close()

    connection, cursor = connect_to_database()

    build_schema(connection, cursor)
    build_dynamic(connection, cursor)

    cursor.close()
    connection.close()


def update_db_schema():
    """Set up or update database schemas from scratch"""

    # Connect to the database provider
    setup_database()

    # Create the database schema
    connection, cursor = connect_to_database()

    build_schema(connection, cursor)
    build_dynamic(connection, cursor)

    # Create secrets file
    secrets_file = open("secrets.txt", "w")

    # Create admin password
    admin_salt = bcrypt.gensalt()
    admin_password = bcrypt.hashpw(b'admin', admin_salt)
    secrets_file.write("admin_password = {}\n".format('admin'))

    # Create guest password
    guest_salt = bcrypt.gensalt()
    guest_password = bcrypt.hashpw(b'guest', guest_salt)
    secrets_file.write("guest_password = {}\n".format('guest'))

    try:
        # Admin has full access
        cursor.execute(
            "INSERT INTO Users (username, password, salt) VALUES (%s, %s, %s)",
            ("admin", admin_password, admin_salt),
        )
        cursor.execute(
            "CREATE USER %s@'localhost' IDENTIFIED BY %s", ('admin', 'admin')
        )
        cursor.execute(
            "GRANT ALL PRIVILEGES ON *.* TO %s@'localhost' WITH GRANT OPTION", ('admin',)
        )

        # Guest has limited access
        cursor.execute(
            "INSERT INTO Users (username, password, salt) VALUES (%s, %s, %s)",
            ("guest", guest_password, guest_salt),
        )
        cursor.execute(
            "CREATE USER %s@'localhost' IDENTIFIED BY %s", ('guest', 'guest')
        )
        cursor.execute(
            "GRANT DROP, INSERT, UPDATE, DELETE, SELECT ON LulaBells.* TO %s@'localhost' WITH GRANT OPTION", ('guest',)
        )
        connection.commit()
    except mysql.connector.Error as error_descriptor:
        print("Failed inserting user: {}".format(error_descriptor))
        cursor.close()
        connection.close()
        exit(1)

 
if __name__ == "__main__":
    update_db_schema()
