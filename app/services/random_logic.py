import logging
import random
from app.utils.exceptions import InvalidURLException
from services.vk_logic import api_VK_client
from utils.parce_url import  VKUrlParser
from api.schemas.schema import Winner,Criteria

# #https://vk.com/wall-228217476_68  https://vk.com/wall-228217476_38  https://vk.com/wall-211669963_1325вот такую ссылку надо парсить


async def choice_winner(
        post_url: str,
        criteria: Criteria,
        count_winners: int,
        required_group: list,
        check_own_group: bool = False,
):  
    #получение айди группы и поста из ссылки на пост ВКонтакте
    group_id, item_id  = VKUrlParser.parse_vk_post(post_url)
    logging.info(f'Получили айди группы и поста: {group_id},{item_id}')

    #логика выборки критериев
    if criteria.likes and criteria.repost and criteria.comments:
        user_ids = set()

        likers = await api_VK_client.get_user_ids_by_likes(group_id,item_id)
        reposters = await api_VK_client.get_user_ids_by_repost(group_id,item_id)
        comments = await api_VK_client.get_user_ids_by_comment(group_id,item_id)

        user_ids.update(likers)
        user_ids.update(reposters)
        user_ids.update(comments)

        user_ids = list(user_ids)
    elif criteria.likes and not criteria.repost and not criteria.comments:
        user_ids = await api_VK_client.get_user_ids_by_likes(group_id,item_id)
    elif not criteria.likes and criteria.repost and not criteria.comments:
        user_ids = await api_VK_client.get_user_ids_by_repost(group_id,item_id)
    elif not criteria.likes and not criteria.repost and criteria.comments:
        user_ids = await api_VK_client.get_user_ids_by_comment(group_id,item_id)

    # проверка на подписку на  группу
    if check_own_group:
        checker = await api_VK_client.check_subscriber(group_id[1:],user_ids)
        logging.info(f'Подписчики группы из активных пост: {checker}')
        user_ids = checker

    # #проверка на подписку на специфические  группы   
    # if required_group:
    #     list_groups_ids = [VKUrlParser.parse_vk_post(group) for group in required_group]
    #     tample_user_ids = set()
    #     for group in list_groups_ids:
    #         checker = await api_VK_client.check_subscriber(group,user_ids)
    
    logging.info(f'Айди пользователей которые удовлетворяют критериям: {user_ids}')
    #находим нужную инфу по списку людей
    participants = await api_VK_client.get_user_info_by_id(user_ids) 

    # логика рандомайзера     
    winner = random.sample(participants, k=count_winners)
    logging.info(f'Победитель конкурса: {winner}')
    return Winner(
        
    )


