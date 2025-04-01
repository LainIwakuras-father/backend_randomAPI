import logging
import random
from services.vk_logic import api_VK_client
from utils.parce_url import  parse_vk_url

# count_winners: int,
#         criteria: dict,
#         required_group: list,
async def choice_winner(
        post_url: str,
) -> str:
    owner_id, item_id  = parse_vk_url(post_url)
    likers = await api_VK_client.get_user_ids_by_likes(owner_id,item_id)
    
    logging.info(f'Лайкнули пост: {likers}')
    checker = await api_VK_client.check_subscriber(owner_id[1:],likers)
    logging.info(f'Подписчики группы из лайкнувших пост: {checker}')
    list_name = await api_VK_client.get_user_info_by_id(checker)
    logging.info(f'Информация о подписчиках группы из лайкнувших пост: {list_name}')
    winner = random.choice(list_name)
    logging.info(f'Победитель конкурса: {winner}')
    return winner


