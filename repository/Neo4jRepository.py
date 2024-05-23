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
