# S3
ACCESS_KEY_ID = ''
ACCESS_SECRET_KEY = ''

# RDS PostgreSQL DB
DBUSER = ''
DBPASS = ''
DBHOST = ''
DBPORT = ''
DBNAME = ''

SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Marshmallow
JSON_SORT_KEYS = False