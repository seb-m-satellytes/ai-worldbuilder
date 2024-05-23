import traceback
from flask import request, jsonify
from repository.Neo4jRepository import Neo4jRepository
from pydantic import ValidationError
from pydantic import BaseModel
from typing import Type

repository: Neo4jRepository = Neo4jRepository()

def shared_get_nodes(model_class: Type[BaseModel]):
    try:
        nodes = repository.get_nodes(model_class)

        if nodes:
            return jsonify({"message": "Found nodes.", "data": nodes}), 200
        else:
            return jsonify({"message": "No results found!", "data": []}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500


def shared_create_node(model_class: Type[BaseModel]):
    data = request.json

    if not data:
        return jsonify({"message": "No data provided!"}), 400
    
    try:
        new_node = model_class(**data)
    except ValidationError as e:
        return jsonify({"message": "Invalid data!", "errors": e.errors()}), 400

    try:
        repository.create_node(new_node)

        return jsonify({"message": "Node created successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failed to create node.", "data": str(e), "trace": tb}), 500
