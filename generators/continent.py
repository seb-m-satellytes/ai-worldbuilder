""" import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 """
import random
import uuid
from generators.country import generate_country
from models.continent import Continent
from controllers.shared import shared_create_node
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()

def allocate_minimum_sizes(num_continents, min_continent_size, total_land_area):
    continents = [min_continent_size] * num_continents
    remaining_land_area = total_land_area - (min_continent_size * num_continents)
    return continents, remaining_land_area

def distribute_remaining_land(continents, remaining_land_area):
    while remaining_land_area > 0:
        for i in range(len(continents)):
            if remaining_land_area <= 0:
                break
            allocation = random.uniform(0, remaining_land_area)
            continents[i] += allocation
            remaining_land_area -= allocation
    return continents

def redistribute_excess_area(continents, max_continent_area):
    excess_area = 0
    for i in range(len(continents)):
        if continents[i] > max_continent_area:
            excess_area += continents[i] - max_continent_area
            continents[i] = max_continent_area
    
    while excess_area > 0:
        for i in range(len(continents)):
            if excess_area <= 0:
                break
            allocation = min(random.uniform(0, excess_area), excess_area)
            if continents[i] + allocation <= max_continent_area:
                continents[i] += allocation
                excess_area -= allocation
    return continents

def generate_continents_by_area(total_land_area, min_continent_size=1_000_000):
    num_continents = random.randint(5, 7)
    min_required_area = min_continent_size * num_continents
    max_continent_area = total_land_area * 0.4

    if min_required_area > total_land_area:
        raise ValueError("Total land area is too small to allocate the minimum required area to each continent.")

    continents, remaining_land_area = allocate_minimum_sizes(num_continents, min_continent_size, total_land_area)
    continents = distribute_remaining_land(continents, remaining_land_area)
    continents = redistribute_excess_area(continents, max_continent_area)
    continents = [Continent(size=round(continent)) for continent in continents]

    return continents

def generate_continents() -> list[Continent]:
    available_surface_area = 510_100_000

    percent_land = random.randint(15, 45) / 100

    # Calculate the surface area of the continent
    total_land_area = available_surface_area * percent_land
    
    continents = generate_continents_by_area(total_land_area)

    print(total_land_area, continents)
    
    for continent in continents:
        continent.world_code = str(uuid.uuid4())
        remaining_land_area = continent.size

        while remaining_land_area >= 300:
            country = generate_country(remaining_land_area)
            if country and country.size <= remaining_land_area:
                continent.countries.append(country)
                remaining_land_area -= country.size
            else:
                continue
    
    return continents

# generated_continents = generate_continents()
# country_count = sum([len(continent.countries) for continent in generated_continents])

""" for continent in generated_continents:
    repository.create_node(continent)
   
    print(f"Continent {continent.world_code} Size: {continent.size} sqkm, Number of Countries: {len(continent.countries)}")
    for country in continent.countries:
        print(f"  Country Size: {country.size} sqkm, Population: {country.population}, Density: {country.density}")
print(f"Continents: {len(generated_continents)} with {country_count} countries")
 """
