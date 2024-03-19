from datetime import datetime
import logging
import configparser
import argparse
import json
import os
import traceback
from pathlib import Path
import app_config


from flask import Flask, jsonify, request, redirect, session, render_template, current_app
from flask_session import Session

from ms_identity_web import IdentityWebPython
from ms_identity_web.adapters import FlaskContextAdapter
from ms_identity_web.errors import NotAuthenticatedError
from ms_identity_web.configuration import AADConfig

import mysql.connector

from database.schema import connect_to_database
from database.insertions import insert_student
from database.retrieval import (
    get_student,
    get_students_for_search_bar,
    get_wardroberental_by_student,
    get_textbookrental_by_student,
    get_textbooks_and_renters,
)
from database.updates import (
    update_pantry_purchase,
    update_rented_cloth_db,
    update_rented_textbook_db,
)
from database.dyn_queries import get_visits_for_student


app = Flask(__name__)
app.secret_key = os.urandom(32)

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")

def create_app(secure_client_credential=None):
    app = Flask(__name__, root_path=Path(__file__).parent)  # initialize Flask app
    app.config.from_object(
        app_config
    )  # load Flask configuration file (e.g., session configs)
    Session(
        app
    )  # init the serverside session for the app: this is requireddue to large cookie size
    aad_configuration = AADConfig.parse_json("aad.config.json")  # parse the aad configs
    app.logger.level = logging.INFO  # can set to DEBUG for verbose logs
    if app.config.get("ENV") == "production":
        # The following is required to run on Azure App Service or any other host with reverse proxy:
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
        # Use client credential from outside the config file, if available.
        if secure_client_credential:
            aad_configuration.client.client_credential = secure_client_credential

    AADConfig.sanity_check_configs(aad_configuration)
    adapter = FlaskContextAdapter(
        app
    )  # ms identity web for python: instantiate the flask adapter
    ms_identity_web = IdentityWebPython(
        aad_configuration, adapter
    )  # then instantiate ms identity web for python

    # Connect to the database
    mydb, mycursor = connect_to_database()

    @app.route("/inventory")
    @ms_identity_web.login_required  
    def main_page():
        return render_template("inventory.html")

    @app.route("/register-student", methods=["POST"])
    @ms_identity_web.login_required
    def register_student():
        data = request.get_json()
        id = data["id"]
        name = data["name"]
        lastName = data["lastName"]
        email = data["email"]
        class_year = data["classYear"]
        residence = data["residence"]
        registration_date = datetime.today().strftime('%Y-%m-%d') 

        # Cleanup Input Data
        if residence == "on-campus":
            residence = 1
        else:
            residence = 0

        # Check if the student is already in the database
        student = get_student(mydb, id)
        if student:
            return jsonify({"message": "Student already in the database"}), 400

        is_inserted = insert_student(mydb, id, name, lastName, email, class_year, residence, registration_date)

        if not is_inserted:
            return jsonify({"message": "Failed to insert student"}), 500

        return jsonify({"message": "Student got inserted"}), 200

    @app.route("/get-search-bar-info", methods=["GET"])
    @ms_identity_web.login_required
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

    @app.route("/get-searched-student-info", methods=["GET"])
    @ms_identity_web.login_required
    def get_searched_student_info():

        student_id = request.args.get('studentId')

        student_info = get_student(mydb, student_id)

        if not student_info:
            return jsonify({"message": "Student does not exist in the database"}), 500

        previous_visits = get_visits_for_student(mydb, student_id)

        if not previous_visits: 
            previous_visits = []

        textbook_rentals = get_textbookrental_by_student(mydb, student_id)

        if not textbook_rentals:
            textbook_rentals = []

        wardrobe_rentals = get_wardroberental_by_student(mydb, student_id)

        if not wardrobe_rentals:
            wardrobe_rentals = []

        result = {
            "studentInfo": student_info,
            "previousVisits": previous_visits,
            "wardrobeRentals": wardrobe_rentals,
            "textbookRentals": textbook_rentals
        }

        return jsonify(result)

    @app.route("/update-grocery-visit", methods=["POST"])
    @ms_identity_web.login_required
    def update_grocery_visit():
        data = request.get_json()
        visitDate = data['visitDate']
        visitDate = datetime.strptime(visitDate, '%m/%d/%Y').strftime('%Y-%m-%d') # Convert to MySQL date format
        visitDetails = data['visitDetails']
        studentInfo = data['student']

        for item in visitDetails:
            item_name = item['itemName']
            quantity = item['itemCount']

            is_updated = update_pantry_purchase(mydb, quantity, visitDate, studentInfo[0], item_name)

            if not is_updated:
                return jsonify({"message": "Failed to update grocery visit"}), 500

        return jsonify({"message": "Grocery visit got inserted"}), 200

    @app.route("/update-rented-cloth", methods=["POST"])
    @ms_identity_web.login_required
    def update_rented_cloth():
        data = request.get_json()
        visitDate = data["visitDate"]
        visitDate = datetime.strptime(visitDate, "%m/%d/%Y").strftime(
            "%Y-%m-%d"
        )  # Convert to MySQL date format
        cloth_id = data["clothId"]
        is_returned = data["isChecked"]
        studentInfo = data["student"]

        is_updated = update_rented_cloth_db(
            mydb, visitDate, studentInfo[0], cloth_id, is_returned
        )

        if not is_updated:
            return jsonify({"message": "Rented Cloth could not be updated"}), 500

        return jsonify({"message": "Rented Cloth has been updated"}), 200

    @app.route("/update-rented-textbook", methods=["POST"])
    @ms_identity_web.login_required
    def update_rented_texbook():
        data = request.get_json()
        print(data)
        visitDate = data["visitDate"]
        visitDate = datetime.strptime(visitDate, "%m/%d/%Y").strftime(
            "%Y-%m-%d"
        )  # Convert to MySQL date format
        textbook_name = data["textbookName"]
        is_returned = data["isChecked"]
        studentInfo = data["student"]

        is_updated = update_rented_textbook_db(
            mydb, visitDate, studentInfo[0], textbook_name, is_returned
        )

        if not is_updated:
            return jsonify({"message": "Rented Textbook could not be updated"}), 500

        return jsonify({"message": "Rented Textbook has been updated"}), 200

    @app.route("/get-textbooks", methods=["GET"])
    @ms_identity_web.login_required
    def get_textbooks():

        print("Getting textbooks")
        result = get_textbooks_and_renters(mydb)

        if (result):
            return jsonify(result)
        
        return jsonify({"message": "Failed to retrieve textbooks"}), 500



    @app.route("/login")
    def login():
        return render_template("login.html")

    @app.route("/")
    def index():
        return render_template("index.html")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=5000, ssl_context="adhoc")

# app = create_app()
