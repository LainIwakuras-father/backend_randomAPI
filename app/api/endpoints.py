
from fastapi import APIRouter, HTTPException

from api.schemas.schema import RaffleRequest, RaffleResponse
from utils.exceptions import handle_http_exceptions
from services.random_logic import choice_winner
from fastapi.responses import FileResponse




router = APIRouter()

@router.get('/')
async def index():
    try:
        return FileResponse('static/index.html')
    except RuntimeError:
         # Обработка, если файл не найден (на всякий случай)
         raise HTTPException(status_code=404, detail="Index.html не найден")

@handle_http_exceptions
@router.post(
    "/get_winners",
    status_code=200,
    response_model=RaffleResponse
)
async def get_winners(raffle:RaffleRequest):
    win =await choice_winner(raffle)
    return RaffleResponse(winner=win)

# @handle_http_exceptions
# @router.post(
#     "/reroll_winner",
#     response_model=RaffleResponse
# )
# async def reroll_winner(request: RerollRequest):
#     return await choice_winner(request)