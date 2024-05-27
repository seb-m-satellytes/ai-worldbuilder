import traceback
from flask import request, jsonify, Blueprint
from models.country import Country
from models.region import Region
from controllers.shared import (
    shared_get_nodes,
    shared_create_node,
    shared_get_children_by_relationship,
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


@country_blueprint.route("/countries/<string:country_id>", methods=['DELETE'])
def delete_country(country_id: str):
    return shared_delete_node(Country, country_id)


@country_blueprint.route("/countries", methods=['DELETE'])
def delete_countries():
    return shared_delete_all_nodes(Country)


@country_blueprint.route("/countries/<string:country_id>/regions", methods=['GET'])
def get_regions(country_id: str):
    return shared_get_children_by_relationship(Country, country_id, "HAS_REGION", Region)


@country_blueprint.route("/countries/<string:country_id>/generate_regions", methods=['POST'])
def generate_regions_route(country_id):
    try:
        country = repository.get_node_by_id(Country, country_id)
        regions = generate_regions(country.get(
            "size"), country.get("population"))

        for region in regions:
            repository.create_node(region)
            repository.create_relationship(
                Country, country_id, Region, region.world_code, "HAS_REGION")

        return jsonify({"message": "Regions generated successfully!", "data": len(regions)}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500


@country_blueprint.route("/countries/<string:country_id>/regions", methods=['DELETE'])
def delete_regions(country_id: str):
    try:
        repository.delete_children_with_relationship(
            Country, country_id, Region, "HAS_REGION")
        return jsonify({"message": "Regions deleted successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500


@country_blueprint.route("/countries/orphans", methods=['DELETE'])
def delete_orphan_countries():
    try:
        repository.delete_orphans_without_relationship(
            Country, "HAS_COUNTRY")
        return jsonify({"message": "Orphan countries deleted successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
