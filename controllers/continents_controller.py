import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_nodes, shared_create_node
from models.continent import Continent
from repository.Neo4jRepository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

continent_blueprint = Blueprint('continent', __name__)

@continent_blueprint.route("/continents", methods=['GET'])
def get_continents():
    return shared_get_nodes(Continent)

    
@continent_blueprint.route("/continents", methods=['POST'])
def create_continent():
   return shared_create_node(request, Continent)

@continent_blueprint.route("/continents/<string:continent_id>", methods=['DELETE'])
def delete_continent(continent_id: str):
    try:
        repository.delete_node(Continent, continent_id)
        return jsonify({"message": "Continent deleted successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
