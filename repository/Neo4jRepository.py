from utils.database import database, driver
from pydantic import BaseModel
from typing import Type
class Neo4jRepository:
    def __init__(self):
        self.driver = driver

    def get_nodes(self, model_class: Type[BaseModel]):
        model_name = model_class.__name__

        try:
            query = f"""
            MATCH (node:{model_name})
            RETURN node
            """
            records, summary, keys = self.driver.execute_query(query, database=database)

            nodes = []
            for record in records:
                node_properties = record.data()["node"]
                nodes.append(node_properties)
            return nodes

        except Exception as e:
            raise e

      
    def create_node(self, model: BaseModel):
        try:
            model_name = model.__class__.__name__
            attributes = model.model_dump()
            attributes_keys = ', '.join(f"{key}: ${key}" for key in attributes.keys())

            query = f"""
            CREATE (node:{model_name} {{{attributes_keys}}})
            RETURN node 
            """

            return self.driver.execute_query(query, **attributes, database_=database)
        except Exception as e:
            raise e

    def delete_node(self, model_class: Type[BaseModel], world_code: str):
        try:
            model_name = model_class.__name__

            query = f"""
            MATCH (node:{model_name} {{world_code: $world_code}})
            DETACH DELETE node
            """
            return self.driver.execute_query(query, world_code=world_code, database_=database)
        except Exception as e:
            raise e

    def create_relationship(self, from_model_class: Type[BaseModel], from_code: str, to_model_class: Type[BaseModel], to_code: str, relationship: str):
        try:
            from_model_name = from_model_class.__name__
            to_model_name = to_model_class.__name__

            query = f"""
            MATCH (from:{from_model_name} {{world_code: $from_code}})
            MATCH (to:{to_model_name} {{world_code: $to_code}})
            CREATE (from)-[:{relationship}]->(to)
            """
            return self.driver.execute_query(query, from_code=from_code, to_code=to_code, database_=database)
        except Exception as e:
            raise e
