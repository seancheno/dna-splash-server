from flask import Flask
from flask_restful import Api
from flask_cors import CORS

import logging

from api.resources.dna import Dna, DnaList
from api.models.create_models import create_models

app = Flask(__name__)

# Create PostgreSQL table
create_models()


@app.before_first_request
def setup_logging():
    if not app.debug:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.INFO)


app.config.from_object('api.config')
# app.config.from_pyfile('api/instance/settings.py')

CORS(app)
api = Api(app)

api.add_resource(Dna, '/create')
api.add_resource(DnaList, '/gallery')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
