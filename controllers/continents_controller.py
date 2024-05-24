import traceback
import logging
from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_nodes, shared_create_node, shared_delete_node, shared_get_node_by_world_id
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

@continent_blueprint.route("/continents/<string:continent_id>", methods=['GET'])
def get_continent(continent_id: str):
   return shared_get_node_by_world_id(Continent, continent_id)

@continent_blueprint.route("/continents/<string:continent_id>", methods=['DELETE'])
def delete_continent(continent_id: str):
   return shared_delete_node(Continent, continent_id)

@continent_blueprint.route("/continents/<string:continent_id>/countries", methods=['GET'])
def get_countries(continent_id: str):
    try:
        # Retrieve the continent from the database
        continent = repository.get_node_by_id(Continent, continent_id)
        
        if continent is None:
            return jsonify({'error': 'Continent not found'}), 404
                
        # Retrieve all countries of the continent
        countries = repository.get_related_nodes(continent, 'HAS_COUNTRY')
                
        if countries:
            return jsonify({"message": f"Found {len(countries)} countries.", "data": countries}), 200
        else:
            return jsonify({"message": "No results found!", "data": []}), 404   
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500
