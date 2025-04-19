import logging
import os

from fastapi.responses import FileResponse
import uvicorn
from api.endpoints import router
from config import loggerConfig
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="Telegram", description="Telegram", version="0.0.1")

origins = [
    "https://web.telegram.org",
    "https://*.telegram.org",
    "null"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],#замени на список доменов, которые могут обращаться к нашему API
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(router=router)

@app.get("/")
def root():
    return FileResponse("static/index.html")
# БЛЯТЬ ПРОБЛЕМА БЫЛА В ОТКЛЮЧЕНИИ КЕША В БРАУЗЕРЕ ctrl +f5 и disable cache Запомни Пожалуйста !!!
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    logging.basicConfig(level=loggerConfig.level, format=loggerConfig.format)
    logging.info("Server is running....")
    uvicorn.run(app, host="127.0.0.1", port=8000)
