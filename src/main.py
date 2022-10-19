import logging

import uvicorn
from fastapi import FastAPI

from fastapi_backend.src.handlers.trades import router as trades_router
from fastapi_backend.src.handlers.users import router as users_router
from fastapi_backend.src.storage.database import Base, engine, database

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(pathname)s] [%(lineno)s] - %(message)s'
)

logger = logging.getLogger("asdf")

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
