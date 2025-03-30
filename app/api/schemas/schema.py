from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class Criteria(BaseModel):
    likes: bool = False
    reposts: bool = False
    comments: bool = False


#Запрос на розыгрыш
class RaffleRequest(BaseModel):
    post_url: HttpUrl
    raffle_name: Optional[str] = None
    count_winners: int
    criteria: Criteria
    required_group: List[HttpUrl]=[]
    check_own_group: bool = False
    own_group_id: Optional[str] = None



class Winner(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    profile_url: str

#Ответ на запрос о розыгрыше
class RaffleResponse(BaseModel):
    winners: List[Winner]
    total_participants: int
    message: Optional[str] = None


class RerollRequest(BaseModel):
    contest_data: RaffleRequest # Исходные данные конкурса
    current_winners: List[Winner] # Текущий список победителей
    winner_to_reroll_id: int # ID пользователя, которого перевыбираем