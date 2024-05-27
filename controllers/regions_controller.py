import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import (
    shared_get_node_by_world_id,
    shared_get_nodes,
    shared_create_node
)
from models.city import City
from models.metropolis import Metropolis
from models.town import Town
from models.village import Village
from models.region import Region
from generators.urban_areas import create_urban_entries
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


@region_blueprint.route("/regions/<string:region_id>/settlements", methods=['GET'])
def get_settlements(region_id):
    settlement_type_models = {
        "city": City,
        "town": Town,
        "metropolis": Metropolis,
        "village": Village,
    }
    try:
        base_node = repository.get_node_by_id(Region, region_id)

        if base_node is None:
            return jsonify({'error': f'{Region.__name__} not found'}), 404

        results = {}

        for settlement_type, model_class in settlement_type_models.items():
            child_nodes = repository.get_related_nodes(
                Region, region_id, "HAS_URBAN_AREA", model_class)

            if child_nodes:
                results[settlement_type] = child_nodes

        if results:
            return jsonify({
                "message": f"Found {len(results)} urban areas.",
                "data": results
            }), 200

        return jsonify({"message": "No results found!", "data": []}), 404

    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500


@region_blueprint.route("/regions/<string:region_id>/create_urban_areas", methods=['POST'])
def create_urban_areas(region_id):
    try:
        region = repository.get_node_by_id(Region, region_id)
        if region is None:
            return jsonify({"error": "Region not found"}), 404

        # Generate urban areas
        metropolises, cities, towns, villages = create_urban_entries(
            region.get("population"), region.get("world_code"))
        return jsonify({
            "message": "Created Urban Areas",
            "data": {
                "metropolises": [metropolis.model_dump() for metropolis in metropolises],
                "cities": [city.model_dump() for city in cities],
                "towns": [town.model_dump() for town in towns],
                "villages": [village.model_dump() for village in villages]
            }
        }), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
