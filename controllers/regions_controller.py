import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_nodes, shared_create_node
from models.region import Region
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

region_blueprint = Blueprint('region', __name__)

@region_blueprint.route("/regions", methods=['GET'])
def get_regions():
    return shared_get_nodes(Region)

    
@region_blueprint.route("/regions", methods=['POST'])
def create_region():
   return shared_create_node(request, Region)


