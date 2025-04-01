import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.endpoints import router

app = FastAPI(
    title="Telegram",
    description="Telegram",
    version="0.0.1",
)

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

path = os.path.join(os.path.dirname(__file__), "static")#ПОЛНЫЙ ПУТЬ К ПАПКЕ STATIC
app.mount("/", StaticFiles(directory=path, html=True), name="static")

app .include_router(router=router)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
