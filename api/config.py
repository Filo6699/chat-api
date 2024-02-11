from decouple import config as env


PSQL_USER = env("POSTGRES_USER")
PSQL_PASSWORD = env("POSTGRES_PASSWORD")
PSQL_DATABASE = env("POSTGRES_DB")
PSQL_HOST = env("POSTGRES_HOST")
PSQL_PORT = env("POSTGRES_PORT")

DATABASE_URL = f"postgresql+asyncpg://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DATABASE}"

JWD_ENCRYPTION_KEY = env("JWD_ENCRYPTION_KEY")
ENCRYPTION_ALGORITHM = env("ENCRYPTION_ALGORITHM")

API_PREFIX = "/api/v1"

username_regex = r'^[\u0020-\u007E]*$'
password_regex = r'^[\u0020-\u007E]*$'
