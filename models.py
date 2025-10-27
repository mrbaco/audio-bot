from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Audio(Base):
    __tablename__ = 'audios'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=True)
    file_name: Mapped[str] = mapped_column(String(128), unique=True, nullable=True)
