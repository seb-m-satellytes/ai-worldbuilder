import random
import math
import uuid
from models.country import Country
    
def generate_country():
    size_min, size_max, size_skew = 300, 10000000, 0.58
    population_min, population_max = 25000, 500000000
    density_min, density_max = 10, 20000

    # Generate random country size (using log-normal distribution)
    size_mu = math.log(size_min) + (math.log(size_max) - math.log(size_min)) * (1 - size_skew)
    size_sigma = (math.log(size_max) - math.log(size_min)) * size_skew
    size = math.exp(random.normalvariate(size_mu, size_sigma))

    # Generate random population density (using log-normal distribution)
    density_mu = math.log((density_min + density_max) / 2)
    density_sigma = math.log(density_max / density_min) / 2
    density = math.exp(random.normalvariate(density_mu, density_sigma))

    # Calculate population
    population = size * density

    # Check if population is within the given range
    if population_min <= population <= population_max and density_min <= density <= density_max:
        return Country(
            world_code=str(uuid.uuid4())[:8],
            name=None,
            size=round(size),
            population=round(population),
            density=round(density)
        )
    else:
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
      print(f"Size: {country[0]:.2f} sq km, Density: {country[1]:.2f} people/sq km, Population: {country[2]:.0f}")
