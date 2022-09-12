import enum

import sqlalchemy
from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID

import uuid

from src.db.database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column("username", sqlalchemy.String)
    full_name = Column("full_name", sqlalchemy.String)
    email = Column("email", sqlalchemy.String)
    hashed_password = Column("hashed_password", sqlalchemy.String)
    disabled = Column("disabled", sqlalchemy.Boolean, default=False)

