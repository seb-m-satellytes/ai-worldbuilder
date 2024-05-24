import traceback
from flask import request, jsonify, Blueprint
from controllers.shared import shared_get_nodes, shared_create_node
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

@world_blueprint.route("/worlds", methods=['POST'])
def create_world():
   return shared_create_node(request, World)
 
@world_blueprint.route("/worlds/<string:world_id>/generate_continents", methods=['POST'])
def generate_continents_route(world_id: str):
    try:
        continents = generate_continents()
        
        for continent in continents:
            continent_without_countries = continent.model_copy()
            
            del continent_without_countries.countries
            repository.create_node(continent_without_countries)
            repository.create_relationship(World, world_id, Continent, continent.world_code, "HAS_CONTINENT")
            
            for country in continent.countries:
                repository.create_node(country)
                repository.create_relationship(Continent, continent.world_code, Country, country.world_code, "HAS_COUNTRY")
        
        return jsonify({"message": "Continents generated successfully!", "data": len(continents)}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
