## Database Folder
This folder contains calls to db and its initial setup. 
There is one important file to run: `setup.py`. It sets up the database from scratch and fills up with some test data. 

Run this file **after**  you set-up the mysql database itself (check the mysql folder)

### DB Operations / Folder Structure
Each DB operation has its own dedicated file. Make sure each procedure follows the same format. 
```
def delete_kitchenware(connection, kitchenware_id):
    """Deletes a kitchenware item from the database"""

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Kitchenware WHERE kitchenware_id = %s", (kitchenware_id,))
        connection.commit()
        cursor.close()
        return True
    except mysql.connector.Error as error_descriptor:
        print("Failed deleting kitchenware item: {}".format(error_descriptor))
        return False
```

Some of the DB calls in this folder are old, so you may need to update them. I modified the schemas a lot, it will most likely be the problem: The function tries to insert into a table (User -> name, surname), but does not have the right values (User -> name, id). 

