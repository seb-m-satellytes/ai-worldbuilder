import random
import math
import uuid

from models.country import Country
from models.continent import Continent


def get_climate_zone(climate_coordinates: int):
    if climate_coordinates in (3, -3):
        return "arctic"

    if climate_coordinates in (2, -2):
        return "temperate"

    if climate_coordinates in (1, -1):
        return "subtropical"

    if climate_coordinates == 0:
        return "tropical"

    return None


def generate_country(remaining_land_area: int, continent: Continent):
    size_min, size_max, size_skew = 1000, 10_000_000, 0.25
    population_min, population_max = 25_000, 500_000_000
    density_min, density_max, density_skew = 10, 10_000, 0.75

    # Generate random country size (using log-normal distribution)
    size_mu = math.log(size_min) + (math.log(size_max) -
                                    math.log(size_min)) * (1 - size_skew)
    size_sigma = (math.log(size_max) - math.log(size_min)) * size_skew
    size = math.exp(random.normalvariate(size_mu, size_sigma))

    size = min(size, remaining_land_area)

    # Generate random population density (using log-normal distribution)
    density_mu = math.log(density_min) + (math.log(density_max) -
                                          math.log(density_min)) * (1 - density_skew)
    density_sigma = (math.log(density_max) -
                     math.log(density_min)) * density_skew
    density = math.exp(random.normalvariate(density_mu, density_sigma))

    # Calculate population
    population = size * density

    climate_coordinates = random.choice(continent.coordinated_at)
    climate_zone = get_climate_zone(climate_coordinates)

    # Check if population is within the given range
    if population_min <= population <= population_max and density_min <= density <= density_max:
        return Country(
            world_code=str(uuid.uuid4()),
            name=None,
            size=int(round(size)),
            population=int(round(population)),
            density=int(round(density)),
            located_at=climate_coordinates,
            climate_zone=climate_zone
        )

    return None


def demo():
    # Generate fictional countries
    countries = []
    while len(countries) < 10:  # Generate 10 fictional countries
        country = generate_country()
        if country:
            countries.append(country)

    # Print the generated countries
    for country in countries:
        print(
            f"Size: {country[0]:.2f} sq km, Density: {country[1]:.2f} people/sq km, Population: {country[2]:.0f}")
