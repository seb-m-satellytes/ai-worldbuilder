import traceback
from flask import request, jsonify, Blueprint
from repository.Neo4jRepository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

city_blueprint = Blueprint('city', __name__)

@city_blueprint.route("/cities", methods=['GET'])
def get_cities():
    try:
        cities, _, _ = repository.get_cities()

        if cities:
            return jsonify({"message": "Cities found!", "data": cities}), 200
        else:
            return jsonify({"message": "No cities found!", "data": []}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failed to get cities.", "data": str(e), "trace": tb}), 500

    
@city_blueprint.route("/cities", methods=['POST'])
def create_city():
    data = request.json

    if not data:
        return jsonify({"message": "No data provided!"}), 400
    
    name = data.get("name")

    try:
        repository.create_city(name)

        return jsonify({"message": "City created successfully!", "data": name}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failed to create city.", "data": str(e), "trace": tb}), 500

    #return jsonify({"message": "City created!"})
