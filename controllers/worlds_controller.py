import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import (
    shared_get_children_by_relationship,
    shared_get_node_by_world_id,
    shared_get_nodes,
    shared_create_node)
from models.world import World
from models.continent import Continent
from models.country import Country
from generators.continent import generate_continents
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

world_blueprint = Blueprint('world', __name__)


@world_blueprint.route("/worlds", methods=['GET'])
def get_worlds():
    return shared_get_nodes(World)


@world_blueprint.route("/worlds/<string:world_id>", methods=['GET'])
def get_world(world_id: str):
    return shared_get_node_by_world_id(World, world_id)


@world_blueprint.route("/worlds/<string:world_id>/continents", methods=['GET'])
def get_continents(world_id: str):
    return shared_get_children_by_relationship(World, world_id, "HAS_CONTINENT", Continent)


@world_blueprint.route("/worlds", methods=['POST'])
def create_world():
    return shared_create_node(request, World)


@world_blueprint.route("/worlds/<string:world_id>/generate_continents", methods=['POST'])
def generate_continents_route(world_id: str):
    try:
        skip_save_flag = request.args.get('SKIP_SAVE', False)
        skip_countries_flag = request.args.get('SKIP_COUNTRIES', False)

        continents = generate_continents(
            generate_countries=not skip_countries_flag)

        global_population = 0

        if not skip_save_flag:
            for continent in continents:
                global_population += sum(
                    country.population for country in continent.countries)

                continent_without_countries = continent.model_copy()

                del continent_without_countries.countries

                repository.create_node(continent_without_countries)
                repository.create_relationship(
                    World, world_id, Continent, continent.world_code, "HAS_CONTINENT")

                for country in continent.countries:
                    repository.create_node(country)
                    repository.create_relationship(
                        Continent, continent.world_code, Country, country.world_code, "HAS_COUNTRY")

        return jsonify({
            "message": "Continents generated successfully!",
            "global_population": f"{global_population:_}",
            "data": [continent.model_dump() for continent in continents]
        }), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500


@world_blueprint.route("/worlds/<string:world_id>/continents", methods=['DELETE'])
def delete_continents(world_id: str):
    try:
        repository.delete_children_with_relationship(
            World, world_id, Continent, "HAS_CONTINENT")

        return jsonify({"message": "Continents deleted successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
