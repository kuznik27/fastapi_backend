import enum

import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, SmallInteger, DateTime, func, Index
from sqlalchemy.dialects.postgresql import UUID

import uuid

from src.db.database import Base


class DealЕype(enum.Enum):
    buy = "buy"
    sell = "sell"


class Trades(Base):
    __tablename__ = "trades"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(sqlalchemy.Enum(DealЕype))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    symbol = Column(sqlalchemy.String)
    price = Column(sqlalchemy.Float)
    timestamp = Column(sqlalchemy.DateTime(timezone=True))

