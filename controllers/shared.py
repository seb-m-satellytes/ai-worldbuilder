import traceback
import uuid
from typing import Type
from flask import jsonify
from pydantic import ValidationError
from pydantic import BaseModel
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()


def validate_request(request, model_class):
    data = request.json

    if not data:
        raise ValueError("No data provided!")

    try:
        return model_class(**data)
    except ValidationError as e:
        raise ValueError(e.json())


def shared_get_nodes(model_class: Type[BaseModel]):
    try:
        nodes = repository.get_nodes(model_class)

        if nodes:
            return jsonify({"message": f"Found {len(nodes)} nodes.", "data": nodes}), 200

        return jsonify({"message": "No results found!", "data": []}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500


def shared_get_children_by_relationship(
    base_model_class: Type[BaseModel],
    world_code: str,
    relationship: str,
    child_model_class: Type[BaseModel]
):
    try:
        # Retrieve the continent from the database
        base_node = repository.get_node_by_id(base_model_class, world_code)

        if base_node is None:
            return jsonify({'error': f'{base_model_class.__name__} not found'}), 404

        # Retrieve all countries of the continent
        node_id = base_node.get('world_code')
        child_nodes = repository.get_related_nodes(
            base_model_class, node_id, relationship)

        if child_nodes:
            return jsonify({
                "message": f"Found {len(child_nodes)} {child_model_class.__name__}(s).",
                "data": child_nodes}), 200

        return jsonify({"message": "No results found!", "data": []}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500


def shared_get_node_by_world_id(model_class: Type[BaseModel], world_code: str):
    try:
        node = repository.get_node_by_id(model_class, world_code)
        if node:
            return jsonify({"message": "Node found.", "data": node}), 200

        return jsonify({"message": "Node not found.", "data": {}}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting node.", "data": str(e), "trace": tb}), 500


def shared_create_node(request, model_class: Type[BaseModel]):
    try:
        new_node = validate_request(request, model_class)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    try:
        if not new_node.world_code:
            new_node.world_code = str(uuid.uuid4())
        repository.create_node(new_node)

        return jsonify({"message": "Node created successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500


def shared_delete_node(model_class: Type[BaseModel], world_code: str):
    try:
        repository.delete_node(model_class, world_code)
        return jsonify({"message": "Node deleted successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500


def shared_delete_all_nodes(model_class: Type[BaseModel]):
    try:
        repository.delete_all_nodes(model_class)
        return jsonify({"message": "All nodes deleted successfully"})
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"error": f"Failed to delete nodes: {e}", 'trace': tb}), 500
