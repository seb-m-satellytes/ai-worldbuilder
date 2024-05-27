import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import (
    shared_get_children_by_relationship,
    shared_get_nodes,
    shared_create_node,
    shared_delete_node,
    shared_get_node_by_world_id)
from models.continent import Continent
from models.country import Country
from repository.neo4j_repository import Neo4jRepository

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
    return shared_get_children_by_relationship(Continent, continent_id, "HAS_COUNTRY", Country)
