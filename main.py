import logging

import uvicorn
from fastapi import FastAPI

from src.db import database
from src.db.database import Base, engine
from src.trades.router import router as trades_router
from src.users.router import router as users_router

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(pathname)s] [%(lineno)s] - %(message)s'
)

logger = logging.getLogger("asdf")

from src.users.models import Users
from src.trades.models import Trades

Base.metadata.create_all(engine)

api = FastAPI()
@api.on_event("startup")
async def startup():
    await database.database.connect()


@api.on_event("shutdown")
async def shutdown():
    await database.database.disconnect()

api.include_router(trades_router)
api.include_router(users_router)

if __name__ == "__main__":
    uvicorn.run(api, host="0.0.0.0", port=8001, debug=True)
