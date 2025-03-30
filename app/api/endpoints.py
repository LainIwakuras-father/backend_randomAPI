
from fastapi import APIRouter

from app.api.schemas.schema import RaffleRequest, RaffleResponse, RerollRequest
from app.utils.exceptions import handle_http_exceptions




router = APIRouter()

@handle_http_exceptions
@router.post("/get_winners",
             response_model=RaffleRequest)
async def get_winners(request: RaffleRequest):
    return {"message": "Hello World"}

@handle_http_exceptions
@router.post("/reroll_winner", response_model=RaffleResponse)
async def reroll_winner(request: RerollRequest):
    return {"message": "Hello World"}