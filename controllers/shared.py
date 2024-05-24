import traceback
import uuid
from flask import request, jsonify
from pydantic import ValidationError
from pydantic import BaseModel
from typing import Type
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
        else:
            return jsonify({"message": "No results found!", "data": []}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500


def shared_get_node_by_world_id(model_class: Type[BaseModel], world_code: str):
    try:
        node = repository.get_node_by_id(model_class, world_code)
        if node:
            return jsonify({"message": "Node found.", "data": node}), 200
        else:
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
        return jsonify({'message': 'All nodes deleted successfully'})
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({'error': 'Failed to delete nodes', 'trace': tb}), 500
