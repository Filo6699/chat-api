from decouple import config as env
from sqlalchemy.pool import QueuePool
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


PSQL_USER = env("POSTGRES_USER")
PSQL_PASSWORD = env("POSTGRES_PASSWORD")
PSQL_DATABASE = env("POSTGRES_DB")

DATABASE_URL = (
    f"postgresql+asyncpg://{PSQL_USER}:{PSQL_PASSWORD}@localhost:5432/{PSQL_DATABASE}"
)

engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = async_sessionmaker(engine)


async def get_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
