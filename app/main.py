import logging
import os

import uvicorn
from api.endpoints import router
from config import loggerConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Telegram", description="Telegram", version="0.0.1")

# origins = [
#     "https://web.telegram.org",
#     "https://*.telegram.org",
#     "null"

# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],#замени на список доменов, которые могут обращаться к нашему API
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )


app.include_router(router=router)


if __name__ == "__main__":
    logging.basicConfig(level=loggerConfig.level, format=loggerConfig.format)
    logging.info("Server is running....")
    uvicorn.run(app, host="127.0.0.1", port=8000)
