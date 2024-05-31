from flask import request, Blueprint, jsonify
from controllers.shared import (
    shared_delete_all_nodes,
    shared_get_nodes,
    shared_get_node_by_world_id
)
from models.city import City
from models.metropolis import Metropolis
from models.town import Town
from models.village import Village
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

settlement_blueprint = Blueprint('settlement', __name__)

settlement_type_models = {
    "city": City,
    "town": Town,
    "metropolis": Metropolis,
    "village": Village,
}


@settlement_blueprint.route("/settlements", methods=['GET'])
def get_settlements():
    settlement_type = request.args.get('settlement_type')
    if not settlement_type:
        return jsonify({"error": "No settlement_type provided"}), 400

    model_class = settlement_type_models.get(settlement_type)

    if not model_class:
        return jsonify({
            "error": f"Invalid settlement_type provided, please use one of: {list(settlement_type_models.keys())}"
        }), 400

    return shared_get_nodes(model_class)


@settlement_blueprint.route("/settlements/<string:settlement_id>", methods=['GET'])
# Not working yet, because shared_ returns a JSON object with a message key
def get_settlement(settlement_id: str):
    for model_class in settlement_type_models.values():
        return shared_get_node_by_world_id(model_class, settlement_id)


@settlement_blueprint.route("/settlements", methods=['DELETE'])
def delete_settlement():
    settlement_type = request.args.get('settlement_type')
    if not settlement_type:
        return jsonify({'error': 'No settlement_type provided'}), 400

    model_class = settlement_type_models.get(settlement_type)

    if not model_class:
        return jsonify({'error': 'Invalid settlement_type provided'}), 400

    return shared_delete_all_nodes(model_class)
