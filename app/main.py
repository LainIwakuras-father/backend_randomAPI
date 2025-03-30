import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.exceptions import HTTPException
from fastapi.responses import FileResponse


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


app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def root():
    try:
        return FileResponse("app/static/index.html")
    except RuntimeError:
         # Обработка, если файл не найден (на всякий случай)
         raise HTTPException(status_code=404, detail="Index.html не найден")



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
    
