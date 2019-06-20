from api.db.base import Base, session

import sqlalchemy as db
from api.aws import s3
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from PIL import Image
import numpy as np
from tqdm import tqdm
from colorutils import Color
import io

import datetime


class DnaModel(Base):

    __tablename__ = 'Dna'

    id = db.Column(db.Integer, primary_key=True)
    animal = db.Column(db.String(100))
    seq_start = db.Column(db.Integer())
    color_values = db.Column(db.ARRAY(db.String(100)))
    dimmensions = db.Column(db.ARRAY(db.Float(precision=2)))
    image_url = db.Column(db.String(200))
    date = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, animal, seq_start, color_values, dimmensions, image_url, uuid):
        self.animal = animal
        self.seq_start = seq_start
        self.color_values = color_values
        self.dimmensions = dimmensions
        self.image_url = image_url
        self.uuid = uuid

        self.rgba_base_pair_map = self.hex_to_rgba(color_values)
        self.width = dimmensions[0]
        self.height = dimmensions[1]

    def load_data(self):
        with open('api/assets/dna/{}.txt'.format(self.animal), 'r') as f:
            base_pair_data = []
            for line in f:
                for c in line.rstrip():
                    base_pair_data.append(c.upper())

        return base_pair_data

    def get_base_pair_seq(self, base_pair_data):
        seq_length = self.width * self.height
        seq_end = (self.seq_start + seq_length) + 25

        base_pair_seq = base_pair_data[self.seq_start: seq_end]

        return base_pair_seq

    def base_pairs_to_rgba(self, base_pair_seq):
        rgba_lists = []
        length = self.width * self.height

        for i in tqdm(range(length)):
            rgba_list = []

            segment = base_pair_seq[i:i + 4]
            for base in segment:

                rgba = self.rgba_base_pair_map[base]
                rgba_list.append(rgba)

            if len(rgba_list) == 4:
                rgba_sum = [(x + y + z) / 4 for x, y,
                            z in zip(rgba_list[0], rgba_list[1], rgba_list[2])]
                rgba_sum.append(255)
                rgba_lists.append(rgba_sum)

        rgba_array = np.array(rgba_lists)

        rgba_array = rgba_array.reshape(
            self.height, self.width, rgba_array.shape[1])

        return rgba_array

    def upload_to_s3(self, rgba_array):
        # Open image
        pil_image = Image.fromarray(rgba_array.astype('uint8'), 'RGBA')

        # Save the image to an in-memory file
        in_mem_file = io.BytesIO()
        pil_image.save(in_mem_file, format="png")
        in_mem_file.seek(0)

        # Upload in_mem_file to S3 as png
        file_name = '{}.png'.format(self.uuid)
        object = s3.Object('dnawebapp', file_name)
        object.put(Body=in_mem_file, ContentType='image/png',
                   ACL='public-read')

    def hex_to_rgba(self, color_values):
        colors = [Color(hex=color_hex) for color_hex in color_values]
        rgba_base_pair_map = {
            'A': colors[0], 'C': colors[1], 'G': colors[2], 'T': colors[3]}
        return rgba_base_pair_map

    @classmethod
    def find_by_name(cls, name):
        insights = session.query(cls).filter_by(name=name)
        return insights

    @classmethod
    def find_all(cls):
        return list(map(lambda x: DnaModel.dump(x), session.query(DnaModel).all()))

    @classmethod
    def dump(cls, dna):
        dna_schema = DnaSchema()
        dna_output = dna_schema.dump(dna).data
        return dna_output

    def save_to_db(self):
        session.add(self)
        session.commit()


class DnaSchema(ModelSchema):
    class Meta:
        ordered = True
    id = fields.Integer()
    animal = fields.Str()
    seq_start = fields.Integer()
    color_values = fields.List(fields.Str())
    dimmensions = fields.List(fields.Float())
    image_url = fields.Str()
    date = fields.Str()
