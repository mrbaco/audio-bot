from typing import AsyncGenerator
from sqlalchemy import Connection, inspect
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

import os

import models

load_dotenv('.env')

DATABASE_URL = os.getenv('DATABASE_CONNECTION_STRING')
if not DATABASE_URL:
    raise ValueError('DATABASE_CONNECTION_STRING не задан в .env')

async_engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session

        except SQLAlchemyError as e:
            await session.rollback()
            raise e

        finally:
            await session.close()

async def create_database():
    async with async_engine.connect() as conn:
        def create_database_if_not_exists(sync_conn: Connection):
            if not inspect(sync_conn).has_table('audios'):
                models.Base.metadata.create_all(bind=sync_conn)
                sync_conn.commit()
                sync_conn.close()

        await conn.run_sync(lambda sync_conn: create_database_if_not_exists(sync_conn))
