import random
import numpy as np

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


def calculate_population(total_population, category, regional_type):
    return total_population * random.uniform(regional_type[category]["min"], regional_type[category]["max"])


def distribute_population_in_category(base_population, stddev, num_units):
    population_values = np.random.normal(base_population, stddev, num_units)
    
    # Ensure all values are positive
    while any(population_values <= 0):
        population_values = np.where(population_values <= 0, np.random.normal(base_population, stddev, 1), population_values)
    
    return population_values


def print_distribution_info(category, units, total_population, distributed_population):
    percentage = distributed_population / total_population
    print(f"{category.capitalize()}: {len(units)} with a total of {distributed_population} people ({percentage:.2f}%)")
    return percentage


def distribute_metropolises(total_population, regional_type):
    metropolitan_population = calculate_population(total_population, "metropolis", regional_type)
    metropolis_base_population = 1_500_000
    no_of_new_metropolises = round(metropolitan_population / metropolis_base_population)
    
    metropolises = []
    metropolitan_population_absolute = 0

    if no_of_new_metropolises > 0:
        new_metropolises = distribute_population_in_category(metropolis_base_population, 350_000, no_of_new_metropolises)
        for new_metropolis in new_metropolises:
            metropolises.append(round(new_metropolis))
            metropolitan_population_absolute += round(new_metropolis)
    
    return metropolises, metropolitan_population_absolute


def distribute_cities(total_population, regional_type):
    cityish_population = calculate_population(total_population, "city", regional_type)
    cityish_base_population = 200_000
    no_of_new_cities = round(cityish_population / cityish_base_population)
    
    cities = []
    cityish_population_absolute = 0
    
    if no_of_new_cities > 0:
        new_cities = distribute_population_in_category(cityish_base_population, 50_000, no_of_new_cities)
        for new_city in new_cities:
            cities.append(round(new_city))
            cityish_population_absolute += round(new_city)
    
    return cities, cityish_population_absolute


def distribute_towns(total_population, regional_type):
    townish_population = calculate_population(total_population, "town", regional_type)
    town_base_population = 20_000
    no_of_new_towns = round(townish_population / town_base_population)
    
    towns = []
    townish_population_absolute = 0
    
    if no_of_new_towns > 0:
        new_towns = distribute_population_in_category(town_base_population, 5_000, no_of_new_towns)
        for new_town in new_towns:
            towns.append(round(new_town))
            townish_population_absolute += round(new_town)
    
    return towns, townish_population_absolute


def distribute_villages(total_population):
    village_base_population = 2000
    no_of_new_villages = round(total_population / village_base_population)
    
    villages = []
    village_population_absolute = 0
    
    if no_of_new_villages > 0:
        new_villages = distribute_population_in_category(village_base_population, 850, no_of_new_villages)
        for new_village in new_villages:
            villages.append(round(new_village))
            village_population_absolute += round(new_village)
    
    return villages, village_population_absolute


def distribute_population(total_population: int):
    regional_type = select_regional_type()
    
    metropolises, metropolitan_population_absolute = distribute_metropolises(total_population, regional_type)
    left_to_distribute = total_population - metropolitan_population_absolute
    
    cities, cityish_population_absolute = distribute_cities(left_to_distribute, regional_type)
    left_to_distribute -= cityish_population_absolute
    
    towns, townish_population_absolute = distribute_towns(left_to_distribute, regional_type)
    left_to_distribute -= townish_population_absolute
    
    villages, village_population_absolute = distribute_villages(left_to_distribute)
    
    met_perc = print_distribution_info("metropolises", metropolises, total_population, metropolitan_population_absolute)
    cit_perc = print_distribution_info("cities", cities, total_population, cityish_population_absolute)
    town_perc = print_distribution_info("towns", towns, total_population, townish_population_absolute)
    vil_perc = print_distribution_info("villages", villages, total_population, village_population_absolute)
    
    print(f"Total: {met_perc + cit_perc + town_perc + vil_perc:.2f}%")
    
    return [metropolises, cities, towns, villages]


# distribute_population(32_129_170)
