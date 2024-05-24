from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_nodes, shared_create_node
from models.city import City
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

city_blueprint = Blueprint('city', __name__)

@city_blueprint.route("/cities", methods=['GET'])
def get_cities():
    return shared_get_nodes(City)

    
@city_blueprint.route("/cities", methods=['POST'])
def create_city():
   return shared_create_node(request, City)
