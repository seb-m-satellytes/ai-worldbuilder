import traceback
from flask import request, jsonify
from repository.Neo4jRepository import Neo4jRepository
from pydantic import ValidationError
from pydantic import BaseModel
from typing import Type

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
            return jsonify({"message": "Found nodes.", "data": nodes}), 200
        else:
            return jsonify({"message": "No results found!", "data": []}), 404
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": "Failure when getting nodes.", "data": str(e), "trace": tb}), 500


def shared_create_node(request, model_class: Type[BaseModel]):
    try:
        new_node = validate_request(request, model_class)
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
   
    try:
        repository.create_node(new_node)

        return jsonify({"message": "Node created successfully!"}), 200
    except Exception as e:
        tb = traceback.format_exc()
        return jsonify({"message": str(e), "trace": tb}), 500
