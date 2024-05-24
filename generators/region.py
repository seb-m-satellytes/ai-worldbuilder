import random
import uuid
import numpy as np
from models.region import Region

def generate_regions(country_size: int, country_population: int):
    if country_size < 1000:
        return None
    if country_size < 10_000:
        regions_min, regions_max = 1, 3
    elif country_size < 100_000:
        regions_min, regions_max = 3, 12
    elif country_size < 1_000_000:
        regions_min, regions_max = 4, 24
    else:
        regions_min, regions_max = 5, 36

    no_of_new_regions = random.randint(regions_min, regions_max)
    
    min_population_per_region = 10000 if country_population >= 20000 else 1000
    
    # Adjust no_of_new_regions to ensure minimum population requirements
    no_of_new_regions = max(1, min(no_of_new_regions, country_population // min_population_per_region))
    
    # Generate Gaussian distributed population values
    mean_population = country_population / no_of_new_regions
    std_dev_population = mean_population / 3  # Arbitrary standard deviation for more variability
    populations = np.random.normal(mean_population, std_dev_population, no_of_new_regions)
    
    # Ensure all populations are positive and meet the minimum population requirement
    populations = np.maximum(populations, min_population_per_region)
    
    # Normalize the populations to ensure their sum equals the total country population
    total_population = np.sum(populations)
    populations = populations * (country_population / total_population)
    
    # Adjust any floating point imprecision by distributing the remaining population
    remaining_population = country_population - int(np.sum(populations))
    for i in range(remaining_population):
        populations[i % no_of_new_regions] += 1
    
    regions = []
    
    for population in populations:
        regions.append(Region(
            world_code=str(uuid.uuid4()),
            population=int(population)
        ))
    
    return regions
