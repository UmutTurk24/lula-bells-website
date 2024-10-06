from datetime import datetime
import logging
import configparser
import argparse
import json
import os
import traceback
from pathlib import Path
# import app_config
from functools import wraps


from flask import (
    Flask,
    jsonify,
    request,
    redirect,
    session,
    render_template,
    current_app,
    redirect,
    url_for,
)
from flask_session import Session
from flask_login import LoginManager, current_user, login_required, login_user, logout_user
from flask_bcrypt import Bcrypt

from ms_identity_web import IdentityWebPython
from ms_identity_web.adapters import FlaskContextAdapter
from ms_identity_web.errors import NotAuthenticatedError
from ms_identity_web.configuration import AADConfig

from static.dist.py import User

import mysql.connector

from database.schema import connect_to_database
from database.insertions import (
    insert_student,
    insert_textbook_rental,
    insert_cloth_rental,
    insert_kitchenware_rental,
    insert_pantry_purchase,
    insert_textbook,
    insert_grocery,
    insert_cloth,
    insert_kitchenware,
)
from database.retrieval import (
    get_student,
    get_students_for_search_bar,
    get_clothrental_by_student,
    get_textbookrental_by_student,
    get_kitchenwarerental_by_student,
    get_textbooks_and_renters,
    get_clothes_and_renters,
    get_kitchenware_and_renters,
    get_grocery_items,
    get_all_textbooks,
    get_all_groceries,
    get_all_clothes,
    get_all_kitchenware,
    get_all_users,
)
from database.updates import (
    update_pantry_purchase,
    update_rented_cloth,
    update_rented_textbook,
    update_rented_kitchenware,
    update_grocery,
    student_agreement,
)

from database.deletions import (
    delete_textbook,
    delete_grocery,
    delete_cloth,
    delete_kitchenware,
)
from database.dyn_queries import get_visits_for_student

app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

ADMIN_NAME = os.environ.get("ADMIN_NAME")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
ADMIN_ID = os.environ.get("ADMIN_ID")
ADMIN_PASSWORD_SALT = os.environ.get("ADMIN_PASSWORD_SALT")


def create_app(secure_client_credential=None):
    app = Flask(__name__, root_path=Path(__file__).parent)  # initialize Flask app

    Session(
        app
    )  # init the serverside session for the app: this is requireddue to large cookie size

    # Flask-login Setup, this is only for the admin page
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_user_by_id(user_id)

    def admin_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != "admin":
                # return redirect(url_for("admin-login"))
                return render_template("admin/login.html")
            return f(*args, **kwargs)

        return decorated_function

    # Flask Bcrypt Setup
    bcrypt = Bcrypt(app)

    # Connect to the database
    mydb = connect_to_database()

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return render_template("index.html")

    @app.route("/volunteer", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            data = request.get_json()

            username = data["username"]
            password = data["password"]

            user = User.get_user_by_username(mydb, username)
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return jsonify({"result": "0"}), 200
            else:
                return jsonify({"result": "1"}), 500

        elif request.method == "GET":
            return render_template("volunteer/login.html")

    @app.route("/inventory")
    @login_required
    def inventory():
        return render_template("volunteer/inventory.html")

    @app.route("/inventory/register-student", methods=["POST"])
    def register_student():
        data = request.get_json()
        id = data["id"]
        name = data["name"]
        lastName = data["lastName"]
        email = data["email"]
        class_year = data["classYear"]
        residence = data["residence"]
        registration_date = datetime.today().strftime("%Y-%m-%d")

        # Cleanup Input Data
        if residence == "on-campus":
            residence = 1
        else:
            residence = 0

        # Check if the student is already in the database
        student = get_student(mydb, id)
        if student:
            return jsonify({"message": "Student already in the database"}), 400

        is_inserted = insert_student(
            mydb, id, name, lastName, email, class_year, residence, registration_date
        )

        if not is_inserted:
            return jsonify({"message": "Failed to insert student"}), 500

        return jsonify({"message": "Student got inserted"}), 200

    @app.route("/inventory/get-search-bar-info", methods=["GET"])
    def get_search_bar_info():

        result = get_students_for_search_bar(mydb)
        if not result:
            return jsonify({"message": "Failed to retrieve students"}), 500

        # Combine the first and last name
        for i in range(len(result)):
            result[i] = (result[i][0], result[i][1] + " " + result[i][2])

        # Append the student id to the name (name + id)
        for i in range(len(result)):
            result[i] = result[i][1] + " " + str(result[i][0])

        return jsonify(result)

    @app.route("/inventory/get-searched-student-info", methods=["GET"])
    def get_searched_student_info():

        student_id = request.args.get("studentId")

        student_info = get_student(mydb, student_id)

        if not student_info:
            return jsonify({"message": "Student does not exist in the database"}), 500

        previous_visits = get_visits_for_student(mydb, student_id)

        if not previous_visits:
            previous_visits = []

        textbook_rentals = get_textbookrental_by_student(mydb, student_id)

        if not textbook_rentals:
            textbook_rentals = []

        cloth_rentals = get_clothrental_by_student(mydb, student_id)

        if not cloth_rentals:
            cloth_rentals = []

        kitchenware_rentals = get_kitchenwarerental_by_student(mydb, student_id)

        if not kitchenware_rentals:
            kitchenware_rentals = []

        result = {
            "studentInfo": student_info,
            "previousVisits": previous_visits,
            "clothRentals": cloth_rentals,
            "textbookRentals": textbook_rentals,
            "kitchenwareRentals": kitchenware_rentals,
        }

        return jsonify(result)

    @app.route("/inventory/update-student-agreement", methods=["POST"])
    def update_student_agreement():
        data = request.get_json()
        student_id = data["studentId"]
        agreement = data["agreement"]

        is_updated = student_agreement(mydb, student_id, agreement)

        if not is_updated:
            return jsonify({"message": "Failed to update student agreement"}), 500

        return jsonify({"message": "Student agreement has been updated"}), 200

    @app.route("/inventory/update-grocery-visit", methods=["POST"])
    def update_grocery_visit():
        data = request.get_json()
        visit_date = data["visitDate"]
        visit_date = datetime.strptime(visit_date, "%m/%d/%Y").strftime(
            "%Y-%m-%d"
        )  # Convert to MySQL date format
        visitDetails = data["visitDetails"]
        studentInfo = data["student"]

        for item in visitDetails:
            item_name = item["itemName"]
            quantity = item["itemCount"]

            is_updated = update_pantry_purchase(
                mydb, quantity, visit_date, studentInfo[0], item_name
            )

            if not is_updated:
                return jsonify({"message": "Failed to update grocery visit"}), 500

        return jsonify({"message": "Grocery visit got inserted"}), 200

    @app.route("/inventory/update-rented-cloth", methods=["POST"])
    def update_rented_cloths():
        data = request.get_json()

        # Convert to MySQL date format
        due_date = data["dueDate"]
        due_date = datetime.strptime(due_date, "%m/%d/%Y").strftime("%Y-%m-%d")

        cloth_id = data["clothId"]
        is_returned = data["isChecked"]
        studentInfo = data["student"]

        is_updated = update_rented_cloth(
            mydb, due_date, studentInfo[0], cloth_id, is_returned
        )

        if not is_updated:
            return jsonify({"message": "Rented Cloth could not be updated"}), 500

        return jsonify({"message": "Rented Cloth has been updated"}), 200

    @app.route("/inventory/update-rented-textbook", methods=["POST"])
    def update_rented_textbooks():
        data = request.get_json()

        due_date = data["dueDate"]
        due_date = datetime.strptime(due_date, "%m/%d/%Y").strftime(
            "%Y-%m-%d"
        )  # Convert to MySQL date format
        textbook_name = data["textbookName"]
        is_returned = data["isChecked"]
        studentInfo = data["student"]

        is_updated = update_rented_textbook(
            mydb, due_date, studentInfo[0], textbook_name, is_returned
        )

        if not is_updated:
            return jsonify({"message": "Rented Textbook could not be updated"}), 500

        return jsonify({"message": "Rented Textbook has been updated"}), 200

    @app.route("/inventory/update-rented-kitchenware", methods=["POST"])
    def update_rented_kitchenwares():
        data = request.get_json()

        due_date = data["dueDate"]
        due_date = datetime.strptime(due_date, "%m/%d/%Y").strftime(
            "%Y-%m-%d"
        )  # Convert to MySQL date format
        kitchenware_name = data["kitchenwareName"]
        is_returned = data["isChecked"]
        studentInfo = data["student"]

        is_updated = update_rented_kitchenware(
            mydb, due_date, studentInfo[0], kitchenware_name, is_returned
        )

        if not is_updated:
            return jsonify({"message": "Rented Textbook could not be updated"}), 500

        return jsonify({"message": "Rented Textbook has been updated"}), 200

    @app.route("/inventory/get-textbooks", methods=["GET"])
    def get_textbooks():

        result = get_textbooks_and_renters(mydb)

        if not result:
            return jsonify({"message": "Failed to retrieve textbooks"}), 500

        return jsonify(result)

    @app.route("/inventory/rent-textbooks", methods=["POST"])
    def rent_textbooks():

        data = request.get_json()

        student_id = data["studentId"]
        textbooks = data["textbooks"]
        due_date = data["dueDate"]

        for textbook in textbooks:
            textbook_name = textbook["name"]

            is_inserted = insert_textbook_rental(
                mydb, student_id, textbook_name, due_date
            )

            if not is_inserted:
                return jsonify({"message": "Failed to rent textbooks"}), 500

        return jsonify({"message": "Textbooks have been rented"}), 200

    @app.route("/inventory/get-clothes", methods=["GET"])
    def get_clothes():

        result = get_clothes_and_renters(mydb)

        if not result:
            return jsonify({"message": "Failed to retrieve textbooks"}), 500

        return jsonify(result)

    @app.route("/inventory/rent-clothes", methods=["POST"])
    def rent_clothes():

        data = request.get_json()

        student_id = data["studentId"]
        clothes = data["clothes"]
        due_date = data["dueDate"]

        for cloth in clothes:
            cloth_name = cloth["name"]

            is_inserted = insert_cloth_rental(mydb, student_id, cloth_name, due_date)

            if not is_inserted:
                return jsonify({"message": "Failed to rent clothes"}), 500

        return jsonify({"message": "Clothes have been rented"}), 200

    @app.route("/inventory/get-kitchenwares", methods=["GET"])
    def get_kitchenwares():

        result = get_kitchenware_and_renters(mydb)

        if not result:
            return jsonify({"message": "Failed to retrieve kitchenware"}), 500

        return jsonify(result)

    @app.route("/inventory/rent-kitchenwares", methods=["POST"])
    def rent_kitchenwares():
        data = request.get_json()

        student_id = data["studentId"]
        kitchenwares = data["kitchenwares"]
        due_date = data["dueDate"]

        for kitchenware in kitchenwares:
            kitchenware_name = kitchenware["name"]

            is_inserted = insert_kitchenware_rental(
                mydb, student_id, kitchenware_name, due_date
            )

            if not is_inserted:
                return jsonify({"message": "Failed to rent clothes"}), 500

        return jsonify({"message": "Clothes have been rented"}), 200

    @app.route("/inventory/get-groceries", methods=["GET"])
    def get_groceries():

        result = get_grocery_items(mydb)

        if not result:
            return jsonify({"message": "Failed to retrieve groceries"}), 500

        return jsonify(result)

    @app.route("/inventory/buy-groceries", methods=["GET"])
    def buy_groceries():
        data = request.get_json()

        student_id = data["studentId"]
        groceries = data["groceries"]

        for grocery in groceries:
            grocery_name = grocery["name"]
            count = grocery["count"]

            is_inserted = insert_pantry_purchase(mydb, student_id, grocery_name, count)

            if not is_inserted:
                return jsonify({"message": "Failed to buy groceries"}), 500

        return jsonify({"message": "Groceries have been bought"}), 200

    @app.route("/admin", methods=["GET", "POST"])
    def admin():
        if request.method == "POST":
            data = request.get_json()

            username = data["username"]
            password = data["password"]

            # Retrieve the salted password from the database
            user = User.get_user_by_username(mydb, username)

            if bcrypt.check_password_hash(user.password, password) and user.role == "admin":
                login_user(user)
                return jsonify({"result": "0"}), 200
            else:
                return jsonify({"result": "1"}), 500

        elif request.method == "GET":
            return render_template("admin/login.html")

    @app.route("/admin/dashboard", methods=["GET"])
    @login_required
    @admin_required
    def admin_page():
        return render_template("admin/dashboard.html")

    @app.route("/admin/dashboard/users", methods=["GET"])
    @login_required
    def user_inventory():
        return render_template("admin/user-inventory.html")

    @app.route("/admin/dashboard/user-inventory", methods=["POST", "GET"])
    # @login_required
    def user_inventory_ends():
        if request.method == "POST":

            changes = request.get_json()['changeList']

            for change in changes:

                if change["opCode"] == 0: # Create
                    salted_password = bcrypt.generate_password_hash(change["password"])
                    print(salted_password)
                    salted_password = salted_password.decode("utf-8")
                    print(salted_password)
                    is_created = User.create_user(
                        mydb, change["username"], salted_password, change["role"]
                    )
                    if not is_created:
                        return jsonify({"message": "Failed to update user"}), 500

                if change["opCode"] == 1: # Delete
                    is_removed = User.delete_user(mydb, change["username"])
                    if not is_removed:
                        return jsonify({"message": "Failed to remove user"}), 500

                if change["opCode"] == 2: # Edit role
                    is_updated = User.update_user_role(mydb, change["username"], change["role"])
                    if not is_updated:
                        return jsonify({"message": "Failed to update user password"}), 500

            return jsonify({"message": "Changes have been processed"}), 200
        elif request.method == "GET":
            result = get_all_users(mydb)

            if not result:
                return jsonify({"message": "Failed to retrieve users"}), 500

            return jsonify(result)

    @app.route("/admin/dashboard/textbooks", methods=["GET"])
    @login_required
    def textbook_inventory():
        return render_template("admin/textbook-inventory.html")

    @app.route("/admin/dashboard/textbook-inventory", methods=["GET", "POST"])
    @login_required
    def textbook_inventory_ends():
        if request.method == "GET":
            result = get_all_textbooks(mydb)

            if not result:
                return jsonify({"message": "Failed to retrieve textbooks"}), 500

            return jsonify(result)
        else:
            items = request.get_json()["changeList"]
            for item in items:
                name = item["name"]
                owned_status = item["ownedStatus"]
                removed = item["removed"]

                if removed:
                    is_removed = delete_textbook(mydb, name)
                    if not is_removed:
                        return jsonify({"message": "Failed to remove textbook"}), 500
                else:
                    is_inserted = insert_textbook(mydb, name, owned_status)
                    if not is_inserted:
                        return jsonify({"message": "Failed to insert textbook"}), 500

            return (
                jsonify(
                    {"message": "Textbooks have been inserted or removed correctly"}
                ),
                200,
            )

    @app.route("/admin/dashboard/grocery", methods=["GET"])
    @login_required
    def grocery_inventory():
        return render_template("admin/grocery-inventory.html")

    @app.route("/admin/dashboard/grocery-inventory", methods=["GET", "POST"])
    @login_required
    def grocery_inventory_ends():
        if request.method == "GET":
            result = get_all_groceries(mydb)

            if not result:
                return jsonify({"message": "Failed to retrieve groceries"}), 500

            return jsonify(result)
        else:
            items = request.get_json()["changeList"]
            for item in items:
                name = item["name"]
                quantity = item["quantity"]
                cost = item["cost"]
                opCode = item["opCode"]

                if opCode == 0:  # Insert
                    is_inserted = insert_grocery(mydb, name, quantity, cost)
                    if not is_inserted:
                        return jsonify({"message": "Failed to insert grocery"}), 500
                elif opCode == 1:  # Delete
                    is_removed = delete_grocery(mydb, name)
                    if not is_removed:
                        return jsonify({"message": "Failed to remove grocery"}), 500
                else:
                    is_updated = update_grocery(mydb, name, quantity, cost)
                    if not is_updated:
                        return jsonify({"message": "Failed to update grocery"}), 500

            return (
                jsonify(
                    {"message": "Groceries have been inserted or removed correctly"}
                ),
                200,
            )

    @app.route("/admin/dashboard/clothes", methods=["GET"])
    @login_required
    def cloth_inventory():
        return render_template("admin/clothing-inventory.html")

    @app.route("/admin/dashboard/cloth-inventory", methods=["GET", "POST"])
    @login_required
    def cloth_inventory_ends():
        if request.method == "GET":
            result = get_all_clothes(mydb)

            if not result:
                return jsonify({"message": "Failed to retrieve clothes"}), 500

            return jsonify(result)
        else:
            items = request.get_json()["changeList"]
            for item in items:
                name = item["name"]
                removed = item["removed"]

                if removed:
                    is_removed = delete_cloth(mydb, name)
                    if not is_removed:
                        return jsonify({"message": "Failed to remove cloth"}), 500
                else:
                    is_inserted = insert_cloth(mydb, name)
                    if not is_inserted:
                        return jsonify({"message": "Failed to insert cloth"}), 500

            return (
                jsonify({"message": "Clothes have been inserted or removed correctly"}),
                200,
            )

    @app.route("/admin/dashboard/kitchenware", methods=["GET"])
    @login_required
    def kitchenware_inventory():
        return render_template("admin/kitchenware-inventory.html")

    @app.route("/admin/dashboard/kitchenware-inventory", methods=["GET", "POST"])
    @login_required
    def kitchenware_inventory_ends():
        if request.method == "GET":
            result = get_all_kitchenware(mydb)

            if not result:
                return jsonify({"message": "Failed to retrieve kitchenware"}), 500

            return jsonify(result)
        else:
            items = request.get_json()["changeList"]
            for item in items:
                name = item["name"]
                removed = item["removed"]

                if removed:
                    is_removed = delete_kitchenware(mydb, name)
                    if not is_removed:
                        return jsonify({"message": "Failed to remove kitchenware"}), 500
                else:
                    is_inserted = insert_kitchenware(mydb, name)
                    if not is_inserted:
                        return jsonify({"message": "Failed to insert kitchenware"}), 500

            return (
                jsonify(
                    {"message": "Kitchenware have been inserted or removed correctly"}
                ),
                200,
            )

    @app.route("/")
    def index():
        return render_template("index.html")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=5000, ssl_context="adhoc")

# app = create_app()
