import os
basedir = os.path.abspath(os.path.dirname(__file__))

if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# DATABASE_URI="postgres+psycopg2://postgres:postgres@localhost:5432/vk"
DATABASE_URI = os.environ['DATABASE_URL']
community_token = os.environ['community_token']
user_token = os.environ['user_token']
