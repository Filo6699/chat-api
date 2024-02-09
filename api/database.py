from decouple import config as env
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from api.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

Base = declarative_base()

SessionLocal = async_sessionmaker(engine)


async def get_session() -> AsyncSession:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
