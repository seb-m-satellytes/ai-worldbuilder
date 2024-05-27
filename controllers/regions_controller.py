import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_node_by_world_id, shared_get_nodes, shared_create_node
from models.region import Region
from generators.urban_areas import distribute_population
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

region_blueprint = Blueprint('region', __name__)


@region_blueprint.route("/regions", methods=['GET'])
def get_regions():
    return shared_get_nodes(Region)


@region_blueprint.route("/regions", methods=['POST'])
def create_region():
    return shared_create_node(request, Region)


@region_blueprint.route("/regions/<string:region_id>", methods=['GET'])
def get_region(region_id):
    return shared_get_node_by_world_id(Region, region_id)


@region_blueprint.route("/regions/<string:region_id>/create_urban_areas", methods=['POST'])
def create_urban_areas(region_id):
    try:
        region = repository.get_node_by_id(Region, region_id)
        if region is None:
            return jsonify({"error": "Region not found"}), 404

        # Generate urban areas
        urban_areas = distribute_population(region.get("population"))
        return jsonify({"message": "Created Urban Areas", "data": urban_areas}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
