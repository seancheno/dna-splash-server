from api.models.dna import DnaModel

from flask import request
from flask_restful import Resource

class Dna(Resource):

    def post(self):
        data = request.get_json()

        width = data['dimmensions']['width']
        height = data['dimmensions']['height']
        a = data['colorValues']['A']
        c = data['colorValues']['C']
        t = data['colorValues']['G']
        g = data['colorValues']['T']

        kwargs = {
            'animal': data['chosenAnimal'],
            'seq_start': data['sliderValue'],
            'color_values': [a, c, t, g],
            'dimmensions': [width, height],
            'uuid': data['uuid'],
            'image_url': data['imageUrl'],
        }
        
        dna = DnaModel(**kwargs)

        base_pair_data = dna.load_data()
        base_pair_seq = dna.get_base_pair_seq(base_pair_data)
        rgba_array = dna.base_pairs_to_rgba(base_pair_seq)
        dna.upload_to_s3(rgba_array)
        dna.save_to_db()

        return kwargs, 201

class DnaList(Resource):
    def get(self):
        return DnaModel.find_all()
