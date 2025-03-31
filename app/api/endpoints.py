
from fastapi import APIRouter

from api.schemas.schema import RaffleRequest, RaffleResponse, RerollRequest
from utils.exceptions import handle_http_exceptions
from services.random_logic import choice_winner




router = APIRouter()

@router.get('/')
async def index():
    return {"message": "Hello World"}

@handle_http_exceptions
@router.post("/get_winners",
             response_model=RaffleRequest)
async def get_winners(request: RaffleRequest):
    return await choice_winner(request)

@handle_http_exceptions
@router.post("/reroll_winner", response_model=RaffleResponse)
async def reroll_winner(request: RerollRequest):
    return await choice_winner(request)