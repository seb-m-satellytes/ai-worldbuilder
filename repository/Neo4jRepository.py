from utils.database import database, driver

class Neo4jRepository:
    def __init__(self):
        self.driver = driver

    # City methods
    def get_cities(self):
        try:
            query = """
            MATCH (city:City)
            RETURN city
            """
            result = self.driver.execute_query(query, database=database)
        except Exception as e:
            raise e

    def create_city(self, name):
      try:
         query = """
          CREATE (city:City {name: $name})
          RETURN city
          """
         return self.driver.execute_query(query, name=name, database_=database)
      except Exception as e:
         raise e
      