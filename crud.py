
from typing import List
from sqlalchemy import delete, select

from database import SessionLocal

import models


async def create(file_id: str, file_name: str) -> bool:
    async with SessionLocal() as session:
        try:
            audio = models.Audio(
                file_id=file_id,
                file_name=file_name
            )

            session.add(audio)

            await session.commit()
            await session.refresh(audio)

            return True

        except Exception as e:
            print(e)
            pass

    return False

async def read_all() -> List[models.Audio]:
    async with SessionLocal() as session:
        try:
            query = select(models.Audio)
            result = await session.execute(query)

            return result.scalars().all()

        except:
            return []

async def read_one(audio_id: (int | None)) -> (models.Audio | None):
    if audio_id:
        async with SessionLocal() as session:
            try:
                query = select(models.Audio).where(models.Audio.id == audio_id)
                result = await session.execute(query)

                return result.scalar_one_or_none()

            except:
                pass

async def remove(audio_id: (int | None)) -> bool:
    if audio_id:
        async with SessionLocal() as session:
            try:
                query = delete(models.Audio).where(models.Audio.id == audio_id)

                await session.execute(query)
                await session.commit()

                return True

            except:
                pass

    return False
