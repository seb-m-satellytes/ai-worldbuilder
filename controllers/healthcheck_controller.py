import logging
import datetime
from flask import Blueprint, jsonify, request
from utils.database import driver

healthcheck_blueprint = Blueprint('healthcheck', __name__)

@healthcheck_blueprint.route("/", methods=['GET'])
def hello():
    return jsonify({"message": f"Hello World! It is now {datetime.datetime.now()}"})

@healthcheck_blueprint.route("/db", methods=['GET'])
def db():
    driver.verify_connectivity()
    return jsonify({"message": "Database is up!"}), 200
