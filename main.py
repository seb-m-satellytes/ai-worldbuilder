import logging
import os
import sys
from flask import Flask
import controllers.healthcheck_controller
import controllers.cities_controller
import controllers.countries_controller
import controllers.worlds_controller
from utils.database import driver

app = Flask(__name__)

app.register_blueprint(controllers.healthcheck_controller.healthcheck_blueprint, url_prefix='/api/v1')
app.register_blueprint(controllers.cities_controller.city_blueprint, url_prefix='/api/v1')
app.register_blueprint(controllers.countries_controller.country_blueprint, url_prefix='/api/v1')
app.register_blueprint(controllers.worlds_controller.world_blueprint, url_prefix='/api/v1')

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
