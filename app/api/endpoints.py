
from fastapi import APIRouter, HTTPException

from api.schemas.schema import RaffleRequest, RaffleResponse
from utils.exceptions import handle_http_exceptions
from services.random_logic import RandomService
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

    win =await RandomService.choice_winner(
                                post_url=str(raffle.post_url),
                                criteria=raffle.criteria,
                                count_winners=raffle.count_winners,
                                check_own_group=raffle.check_own_group,
                                )
    return RaffleResponse(winners=win)
