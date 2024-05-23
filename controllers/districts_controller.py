import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_nodes, shared_create_node
from models.district import District
from repository.Neo4jRepository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

district_blueprint = Blueprint('district', __name__)

@district_blueprint.route("/districts", methods=['GET'])
def get_districts():
    return shared_get_nodes(District)

    
@district_blueprint.route("/districts", methods=['POST'])
def create_district():
   return shared_create_node(request, District)
