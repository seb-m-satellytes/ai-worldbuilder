import logging
import os
import sys
from flask import Flask
from controllers.healthcheck_controller import healthcheck_blueprint
from controllers.cities_controller import city_blueprint
from controllers.countries_controller import country_blueprint
from controllers.worlds_controller import world_blueprint
from controllers.continents_controller import continent_blueprint
from controllers.regions_controller import region_blueprint
from utils.database import driver

app = Flask(__name__)

URL_PREFIX = '/api/v1'

def register_blueprints(app_instance):
    blueprints = [
        (healthcheck_blueprint, URL_PREFIX),
        (city_blueprint, URL_PREFIX),
        (country_blueprint, URL_PREFIX),
        (world_blueprint, URL_PREFIX),
        (continent_blueprint, URL_PREFIX),
        (region_blueprint, URL_PREFIX)
    ]

    for blueprint, url_prefix in blueprints:
        app_instance.register_blueprint(blueprint, url_prefix=url_prefix)

register_blueprints(app)

if __name__ == "__main__":
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    logging.getLogger("neo4j").addHandler(handler)
    logging.getLogger("neo4j").setLevel(logging.DEBUG)

    logging.root.setLevel(logging.INFO)
    logging.info("Starting on port %d", 8080)
    try:
        app.run(debug=True, host="0.0.0.0", port=int(
            os.environ.get("PORT", 8080)))
    finally:
        driver.close()
