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
            records, summary, keys = self.driver.execute_query(query, database=database)

            cities = []
            
            for record in records:
                city_properties = record.data()["city"]
                cities.append(city_properties)
            return cities

        except Exception as e:
            raise e

    def create_city(
            self, 
            name, 
            population, 
            year_first_mentioned):
      try:
         query = """
          CREATE (city:City {name: $name, population: $population, year_first_mentioned: $year_first_mentioned})
          RETURN city
          """
         return self.driver.execute_query(query, 
                                          name=name, 
                                          population=population, 
                                          year_first_mentioned=year_first_mentioned, 
                                          database_=database)
      except Exception as e:
         raise e
      