import logging
import os
import sys
from flask import Flask
from controllers import healthcheck_controller, cities_controller
from utils.database import driver

app = Flask(__name__)

app.register_blueprint(healthcheck_controller.healthcheck_blueprint, url_prefix='/api/v1')
app.register_blueprint(cities_controller.city_blueprint, url_prefix='/api/v1')

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
