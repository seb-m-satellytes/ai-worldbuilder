import random
import uuid

from generators.country import generate_country
from models.continent import Continent
from repository.neo4j_repository import Neo4jRepository

repository: Neo4jRepository = Neo4jRepository()


def allocate_minimum_sizes(num_continents, min_continent_size, total_land_area):
    continents = [min_continent_size] * num_continents
    remaining_land_area = total_land_area - \
        (min_continent_size * num_continents)
    return continents, remaining_land_area


def distribute_remaining_land(continents, remaining_land_area):
    while remaining_land_area > 0:
        for [i, _] in enumerate(continents):
            if remaining_land_area <= 0:
                break
            allocation = random.uniform(0, remaining_land_area)
            continents[i] += allocation
            remaining_land_area -= allocation
    return continents


def redistribute_excess_area(continents, max_continent_area):
    excess_area = 0
    for [i, _] in enumerate(continents):
        if continents[i] > max_continent_area:
            excess_area += continents[i] - max_continent_area
            continents[i] = max_continent_area

    while excess_area > 0:
        for [i, _] in enumerate(continents):
            if excess_area <= 0:
                break
            allocation = min(random.uniform(0, excess_area), excess_area)
            if continents[i] + allocation <= max_continent_area:
                continents[i] += allocation
                excess_area -= allocation
    return continents


def generate_continents_by_area(total_land_area, min_continent_size=1_000_000) -> list[int]:
    num_continents = random.randint(5, 7)
    min_required_area = min_continent_size * num_continents
    max_continent_area = total_land_area * 0.4

    if min_required_area > total_land_area:
        raise ValueError(
            "Total land area is too small to allocate the minimum required area to each continent.")

    continents, remaining_land_area = allocate_minimum_sizes(
        num_continents, min_continent_size, total_land_area)
    continents = distribute_remaining_land(continents, remaining_land_area)
    continents = redistribute_excess_area(continents, max_continent_area)

    return continents


def set_category_and_coordinates(continents) -> list[Continent]:
    continents_models = []

    for continent in continents:
        category = ""
        size_s = 10_000_000
        size_m = 25_000_000
        size_l = 40_000_000

        s_coordinates = [(3, 3), (2, 2), (1, 1), (0, 0),
                         (-1, -1), (-2, -2), (-3, -3)]
        m_coordinates = [(3, 2), (2, 1), (1, 0), (0, -1), (-1, -2), (-2, -3)]
        l_coordinates = [(3, 2, 1), (2, 1, 0), (1, 0, -1),
                         (0, -1, -2), (-1, -2, -3)]
        xl_coordinates = [(3, 2, 1, 0), (2, 1, 0, -1),
                          (1, 0, -1, -2), (0, -1, -2, -3)]

        if continent < size_s:
            category = "small"
            coordinated_at = random.choice(s_coordinates)
        elif continent < size_m:
            category = "medium"
            coordinated_at = random.choice(m_coordinates)
        elif continent < size_l:
            category = "large"
            coordinated_at = random.choice(l_coordinates)
        else:
            category = "extra-large"
            coordinated_at = random.choice(xl_coordinates)

        north_bound = coordinated_at[0]
        south_bound = coordinated_at[-1]

        # use a 20% chance that the continent is an island chain
        is_island = random.choice([True, False, False, False, False])

        continents_models.append(Continent(
            world_code=str(uuid.uuid4()),
            size=round(continent),
            category=category,
            coordinated_at=coordinated_at,
            north_bound=north_bound,
            south_bound=south_bound,
            is_island=is_island
        ))

    return continents_models


def generate_continents(generate_countries: bool) -> list[Continent]:
    available_surface_area = 510_100_000

    percent_land = random.randint(15, 30) / 100

    # Calculate the surface area of the continent
    total_land_area = available_surface_area * percent_land

    continents = generate_continents_by_area(total_land_area)
    continents_as_models = set_category_and_coordinates(continents)

    for continent in continents_as_models:
        remaining_land_area = continent.size

        if generate_countries:
            while remaining_land_area >= 300:
                country = generate_country(remaining_land_area, continent)
                if country and country.size <= remaining_land_area:
                    continent.countries.append(country)
                    remaining_land_area -= country.size
                else:
                    continue

    return continents_as_models
