from api import config
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = db.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()