import traceback
from flask import request, jsonify, Blueprint
from models.country import Country
from models.region import Region
from controllers.shared import (
    shared_get_nodes,
    shared_create_node,
    shared_delete_node,
    shared_delete_all_nodes)
from repository.neo4j_repository import Neo4jRepository
from generators.region import generate_regions

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

@country_blueprint.route("/countries/<string:world_code>/generate_regions", methods=['POST'])
def generate_regions_route(world_code):
    try:
        country = repository.get_node_by_id(Country, world_code)
        regions = generate_regions(country.get("size"), country.get("population"))
        
        for region in regions:
            repository.create_node(region)
            repository.create_relationship(Country, world_code, Region, region.world_code, "HAS_REGION")
            
        return jsonify({"message": "Regions generated successfully!", "data": len(regions)}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
    
@country_blueprint.route("/countries/<string:world_code>/regions", methods=['DELETE'])
def delete_regions(world_code: str):
    try:
        repository.delete_children_with_relationship(Country, world_code, Region, "HAS_REGION")
        return jsonify({"message": "Regions deleted successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
