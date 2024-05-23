import random
from country import generate_country

def generate_continent():
  min_countries, max_countries = 1, 35

  # Generate random number of countries
  countries = []
  num_countries = random.randint(min_countries, max_countries)

  # Generate fictional countries
  while len(countries) < num_countries:
      country = generate_country()
      if country:
          countries.append(country)

  return countries

gen_count = generate_continent()
print(gen_count)
