from api.schemas.schema import RaffleRequest, RaffleResponse
from fastapi import APIRouter
from fastapi.responses import FileResponse
from services.random_logic import RandomService
from utils.exceptions import handle_http_exceptions

router = APIRouter()


@handle_http_exceptions
@router.post("/get_winners", status_code=200, response_model=RaffleResponse)
async def get_winners(raffle: RaffleRequest):

    win = await RandomService.choice_winner(
        post_url=raffle.post_url,
        criteria=raffle.criteria,
        count_winners=raffle.count_winners,
        check_own_group=raffle.check_own_group,
        required_group=raffle.required_group,
    )
    return RaffleResponse(winners=win)

#доделать еще одну функцию для повторной рандомизации 
@handle_http_exceptions
@router.post("/get_reroll", status_code=200, response_model=RaffleResponse)
async def get_winners(raffle: RaffleRequest):

    win = await RandomService.choice_winner(
        post_url=raffle.post_url,
        criteria=raffle.criteria,
        count_winners=raffle.count_winners,
        check_own_group=raffle.check_own_group,
    )
    return RaffleResponse(winners=win)
