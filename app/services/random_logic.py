import logging
import random

from fastapi import HTTPException
from utils.exceptions import InvalidURLException
from services.vk_logic import api_VK_client
from utils.parce_url import  VKUrlParser
from api.schemas.schema import Winner,Criteria


class RandomService:
    """
    Класс для работы с логикой рандомайзера.
    """
    @staticmethod
    async def choice_winner(
            post_url: str,
            criteria: Criteria,
            count_winners: int,
            required_group: list = [],
            check_own_group: bool = False,
    ):  
        #получение айди группы и поста из ссылки на пост ВКонтакте
        group_id, item_id  = VKUrlParser.parse_vk_post(post_url)
        logging.info(f'Получили айди группы и поста: {group_id},{item_id}')

        #логика выборки критериев
        if criteria.likes and criteria.reposts and criteria.comments:
            user_ids = set()

            likers = await api_VK_client.get_user_ids_by_likes(group_id,item_id)
            reposters = await api_VK_client.get_user_ids_by_repost(group_id,item_id)
            comments = await api_VK_client.get_user_ids_by_comment(group_id,item_id,)

            user_ids.update(likers)
            user_ids.update(reposters)
            user_ids.update(comments)

            user_ids = list(user_ids)
        elif criteria.likes and not criteria.reposts and not criteria.comments:
            user_ids = await api_VK_client.get_user_ids_by_likes(group_id,item_id)
        elif not criteria.likes and criteria.reposts and not criteria.comments:
            user_ids = await api_VK_client.get_user_ids_by_repost(group_id,item_id)
        elif not criteria.likes and not criteria.reposts and criteria.comments:
            user_ids = await api_VK_client.get_user_ids_by_comment(group_id,item_id)
        else:
            raise HTTPException(status_code=422,detail="Неверная комбинация критериев. Выберите хотя бы один критерий.")
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
        
        # логика рандомайзера     
        participants = random.sample(user_ids, k=count_winners)
        logging.info(f'Победитель конкурса: {participants}')

        #находим нужную инфу по списку людей
        winner = await api_VK_client.get_user_info_by_id(participants) 
        logging.info(f'Победитель конкурса: {winner}')
        return winner

        


