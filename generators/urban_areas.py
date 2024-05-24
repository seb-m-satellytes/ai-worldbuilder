import numpy as np
import random

def select_regional_type():
    regions = {
        "rural": {
            "metropolis": {"min": 0.00, "max": 0.10},
            "city": {"min": 0.10, "max": 0.15},
            "town": {"min": 0.15, "max": 0.20}
        },
        "urbanized": {
            "metropolis": {"min": 0.10, "max": 0.15},
            "city": {"min": 0.20, "max": 0.30},
            "town": {"min": 0.30, "max": 0.35}
        },
        "metropolized": {
            "metropolis": {"min": 0.35, "max": 0.52},
            "city": {"min": 0.30, "max": 0.48},
            "town": {"min": 0.40, "max": 0.55}
        }
    }
    
    # Select a random regional type from the available types
    selected_type = random.choice(list(regions.keys()))
    return regions[selected_type]
    

def distribute_population(total_population: int):
    regional_type = select_regional_type()
    metropolitan_population = total_population * random.uniform(regional_type["metropolis"]["min"], regional_type["metropolis"]["max"])
    metropolis_base_population = 1_500_000
    
    no_of_new_metropolises = round(metropolitan_population / metropolis_base_population)
    
    metropolises = []
    left_to_distribute = total_population
    metropolitan_population_absolute = 0

    if no_of_new_metropolises > 0:
        new_metropolises = np.random.normal(metropolis_base_population, 350_000, no_of_new_metropolises)
        
        for new_metropolis in new_metropolises:
            metropolises.append(round(new_metropolis))
            left_to_distribute -= round(new_metropolis)
            metropolitan_population_absolute += round(new_metropolis)
        
        met_perc = metropolitan_population_absolute / total_population
    else:
        met_perc = 0
    
    print(f"Metropolises: {len(metropolises)} with a total of {metropolitan_population_absolute} people ( {met_perc:2f} %)")
    
    cityish_population = left_to_distribute * random.uniform(regional_type["city"]["min"], regional_type["city"]["max"])
    cityish_base_population = 200_000
    no_of_new_cities = round(cityish_population / cityish_base_population)
    
    cities = []
    cityish_population_absolute = 0
    
    if no_of_new_cities > 0:
        new_cities = np.random.normal(cityish_base_population, 50_000, no_of_new_cities)
        
        for new_city in new_cities:
            cities.append(round(new_city))
            left_to_distribute -= round(new_city)
            cityish_population_absolute += round(new_city)
        
        cit_perc = cityish_population_absolute / total_population
    else:
        cit_perc = 0
        
    print(f"Cities: {len(cities)} with a total of {cityish_population_absolute} people ( {cit_perc:2f} %)")
    
    townish_population = left_to_distribute * random.uniform(regional_type["town"]["min"], regional_type["town"]["max"])
    town_base_population = 20_000
    no_of_new_towns = round(townish_population / town_base_population)
    
    towns = []
    townish_population_absolute = 0
    
    if no_of_new_towns > 0:
        new_towns = np.random.normal(town_base_population, 5_000, no_of_new_towns)
        
        for new_town in new_towns:
            towns.append(round(new_town))
            left_to_distribute -= round(new_town)
            townish_population_absolute += round(new_town)
        
        town_perc = townish_population_absolute / total_population
    else:
        town_perc = 0
        
    print(f"Towns: {len(towns)} with a total of {townish_population_absolute} people ( {town_perc:2f} %)")

    villages_population = left_to_distribute
    village_base_population = 2000
    no_of_new_villages = round(villages_population / village_base_population)
    
    villages = []
    village_population_absolute = 0
    
    if no_of_new_villages > 0:
        new_villages = np.random.normal(village_base_population, 500, no_of_new_villages)
        
        for new_village in new_villages:
            villages.append(round(new_village))
            left_to_distribute -= round(new_village)
            village_population_absolute += round(new_village)
        
        vil_perc = village_population_absolute / total_population
    else:
        vil_perc = 0
        
    print(f"Villages: {len(villages)} with a total of {village_population_absolute} people ( {vil_perc:2f} %)")
    
    print(f"{met_perc + cit_perc + town_perc + vil_perc}")
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

