import numpy as np
import random

def distribute_population(total_population: int):
    # metropolises = 0
    cities = 0
    towns = 0
    villages = 0
    
    metropolitan_population = total_population * random.uniform(0.20, 0.30)
    cities_population = total_population * 0.08
    towns_population = total_population * 0.27
    villages_population = total_population * 0.63
    
    no_of_new_metropolises = round(metropolitan_population / 1_500_000)
    
    metropolises = []
    left_to_distribute = total_population
    metropolitan_population_absolute = 0

    if no_of_new_metropolises > 0:
        new_metropolises = np.random.normal(1_500_000, 350_000, no_of_new_metropolises)
        
        for new_metropolis in new_metropolises:
            metropolises.append(round(new_metropolis))
            left_to_distribute -= round(new_metropolis)
            metropolitan_population_absolute += round(new_metropolis)
        
        perc = metropolitan_population_absolute / total_population
    else:
        perc = 0
    
    print(f"Metropolises: {len(metropolises)} with a total of {metropolitan_population_absolute} people ( {perc:2f} %)")
    return ""
   
    
    if total_population < 10_000:
        towns = max(1, round(total_population / 1_000))
    else:
        metropolises = max(1, round(metropolises_population / 1_000_000))
        # Assuming a city has 100,000 people
        cities = max(1, round(cities_population / 100_000))
        # Assuming a town has 10,000 people
        towns = max(1, round(towns_population / 10_000))
        # Assuming a village has 100 people
        villages = max(1, round(villages_population / 100))
    

    print(f"Metropolises: {metropolises} with {metropolises_population} people")
    print(f"Cities: {cities} with {cities_population} people")
    print(f"Towns: {towns} with {towns_population} people")
    print(f"Villages: {villages} with {villages_population} people")
    
distribute_population(129_170)
distribute_population(629_170)
distribute_population(1_129_170)
distribute_population(2_129_170)
distribute_population(4_129_170)
distribute_population(8_129_170)
distribute_population(16_129_170)
distribute_population(32_129_170)
distribute_population(64_129_170)
distribute_population(128_129_170)

