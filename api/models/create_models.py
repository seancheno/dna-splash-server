from api.db.base import engine
from api.models.dna import DnaModel

def create_models():
    DnaModel.__table__.drop(engine)
    DnaModel.__table__.create(engine)