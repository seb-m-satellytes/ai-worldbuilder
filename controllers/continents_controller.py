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
