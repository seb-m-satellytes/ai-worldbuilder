import traceback
from flask import request, jsonify, Blueprint
from pydantic import ValidationError
from models.country import Country
from controllers.shared import shared_get_nodes, shared_create_node, shared_delete_node, shared_delete_all_nodes
from repository.Neo4jRepository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

country_blueprint = Blueprint('country', __name__)

@country_blueprint.route("/countries", methods=['GET'])
def get_countries():
    return shared_get_nodes(Country)
    
@country_blueprint.route("/countries", methods=['POST'])
def create_country():
    return shared_create_node(request, Country)

@country_blueprint.route("/countries/<string:world_code>", methods=['DELETE'])
def delete_country(world_code: str):
    return shared_delete_node(Country, world_code)

@country_blueprint.route("/countries", methods=['DELETE'])
def delete_countries():
    return shared_delete_all_nodes(Country)
