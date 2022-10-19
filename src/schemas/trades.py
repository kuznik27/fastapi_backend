import enum
from datetime import datetime

from pydantic import BaseModel, UUID4


class Trade(BaseModel):
    type: str
    user_id: UUID4
    symbol: str
    price: float
    timestamp: datetime


class TradeOut(BaseModel):
    id: UUID4
    type: str
    user_id: UUID4
    symbol: str
    price: float
    timestamp: datetime


class TradeRangeOut(BaseModel):
    symbol: str
    max: float
    min: float


class SymbolType(enum.Enum):
    brc = "btc"
    eth = "eth"
    abx = "abx"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_