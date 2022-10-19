import uuid
from typing import Union

from fastapi import APIRouter, Depends, Query

from fastapi_backend.config.dependencies import oauth2_scheme
from fastapi_backend.src.storage.database import database
from fastapi_backend.src.storage.schemas.trades import TradeOut, Trade, TradeRangeOut

router = APIRouter(
    prefix="/stocks",
    tags=["trades"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.delete("/")
async def delete_trades():
    s = "DELETE FROM trades"
    return await database.database.fetch_all(s)


@router.post("/")
async def create_trades(trade: Trade):
    s = "INSERT INTO trades(id,type,user_id,symbol,price,timestamp) VALUES (:id,:type,:user_id,:symbol,:price,:timestamp)"
    values = trade.dict()
    values.update({"id": uuid.uuid4()})
    return await database.database.execute(query=s, values=values)


@router.get("/", response_model=list[TradeOut])
async def get_trades(user_id: Union[str, None] = None):
    query = "SELECT * FROM trades"
    if user_id:
        query = f"{query} WHERE user_id='{user_id}'"
    rows = await database.database.fetch_all(query=query)
    return rows


@router.get("/{symbol}/price", response_model=Union[TradeRangeOut, dict])
async def get_trades(
        symbol: str,
        start_date: str = Query(..., regex=r"[\d]{4}-[\d]{1,2}-[\d]{1,2}"),
        end_date: str = Query(..., regex=r"[\d]{4}-[\d]{1,2}-[\d]{1,2}")):
    query = "SELECT DISTINCT(symbol) FROM trades"
    avaliable_symbols = await database.database.fetch_all(query=query)
    avaliable_symbols = [i.symbol for i in avaliable_symbols]
    if symbol in avaliable_symbols:
        query = "SELECT MAX(price), MIN(price) FROM trades"
        start_date = f"{start_date} 00:00:00"
        end_date = f"{end_date} 00:00:00"
        query = f"{query} WHERE symbol='{symbol}' and timestamp BETWEEN '{start_date}' AND '{end_date}' "
        rows = await database.database.fetch_one(query=query)
        try:
            return TradeRangeOut(symbol=symbol, min=rows.min, max=rows.max).dict()
        except:
            return {"message": "Нет сделок в заданном периоде"}
    else:
        return {"message": f"Сделок с символом {symbol} не существует"}
