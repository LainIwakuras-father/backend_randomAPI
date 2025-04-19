from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class Criteria(BaseModel):
    likes: bool = False
    reposts: bool = False
    comments: bool = False


# Запрос на розыгрыш
class RaffleRequest(BaseModel):
    post_url: HttpUrl
    raffle_name: Optional[str] = None
    criteria: Criteria
    required_groups: List[HttpUrl] = []
    check_own_group: bool = False
    count_winners: int = Field(ge=1)

class Winner(BaseModel):
    first_name: str
    last_name: str
    profile_url: str


# Ответ на запрос о розыгрыше
class RaffleResponse(BaseModel):
    msg: str = "Конкурс успешно проведен!"
    winners: List[Winner]
    # total_participants: int


# class RerollRequest(BaseModel):
#     contest_data: RaffleRequest # Исходные данные конкурса
#     current_winners: List[Winner] # Текущий список победителей
#     winner_to_reroll_id: int # ID пользователя, которого перевыбираем
