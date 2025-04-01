
from fastapi import APIRouter

from api.schemas.schema import RaffleRequest, RaffleResponse, RerollRequest
from utils.exceptions import handle_http_exceptions
from services.random_logic import choice_winner
from fastapi.responses import FileResponse




router = APIRouter()

# @router.get('/')
# async def index():
#     return FileResponse("app/static/index.html")

@handle_http_exceptions
@router.post("/get_winners")
async def get_winners(post_url: str):
    win =await choice_winner(post_url)
    return {"Победитель конкурса": win}

@handle_http_exceptions
@router.post("/reroll_winner", response_model=RaffleResponse)
async def reroll_winner(request: RerollRequest):
    return await choice_winner(request)