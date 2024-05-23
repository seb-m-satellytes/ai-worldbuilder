import traceback
from flask import request, jsonify, Blueprint
from pydantic import ValidationError
from models.country import Country
from controllers.shared import shared_get_nodes, shared_create_node
from repository.Neo4jRepository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

country_blueprint = Blueprint('country', __name__)

@country_blueprint.route("/countries", methods=['GET'])
def get_countries():
    return shared_get_nodes(Country)
    
@country_blueprint.route("/countries", methods=['POST'])
def create_country():
    return shared_create_node(Country)
