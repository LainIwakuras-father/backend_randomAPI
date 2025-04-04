import asyncio
import logging
import random
from typing import List

import aiohttp
from api.schemas.schema import Winner
from config import VK_TOKEN
from utils.exceptions import VKAPIError


class api_VK_client:

    @staticmethod
    async def make_request(method: str, params):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(
                    f"https://api.vk.com/method/{method}", params=params
                ) as response:
                    result = await response.json()
                    if "error" in result:
                        error_code = result["error"]["error_code"]
                        error_msg = result["error"]["error_msg"]
                        raise VKAPIError(f"VK API Error ({error_code}): {error_msg}")
                    return result
            except aiohttp.ClientError as e:
                logging.error(f"Сетевая ошибка при запросе API ВКонтакте:: {e}")
                raise VKAPIError(f"Сетевая ошибка при запросе API ВКонтакте:: {e}")

    @staticmethod
    async def get_club_by_id(group_screen_name: str, vk_token: str = VK_TOKEN):
        """
        Возвращает айди группы по её ссылке c названием
        """
        params = {
            "group_id": group_screen_name,
            "access_token": vk_token,
            "v": "5.199",
        }
        res = await api_VK_client.make_request("groups.getById", params)
        return res["response"]["groups"][0]["id"]

    @staticmethod
    async def get_user_ids_by_likes(
        owner_id: str, item_id: str, vk_token=VK_TOKEN
    ) -> list[int]:
        """
        Возращает список айди пользователей,
        которые лайкнули  пост Вконтанке
        """
        params = {
            "type": "post",
            "owner_id": owner_id,
            "item_id": item_id,
            "access_token": vk_token,
            "v": "5.199",
        }
        result = await api_VK_client.make_request("likes.getList", params)
        logging.info("посмотрел лайки")
        return result["response"]["items"]

    @staticmethod
    async def get_user_ids_by_repost(
        owner_id: str, post_id: str, vk_token=VK_TOKEN
    ) -> list[int]:
        """
        Возращает список айди пользователей,
        которые репостнули  пост Вконтанке
        """
        params = {
            "owner_id": owner_id,
            "post_id": post_id,
            "access_token": vk_token,
            "v": "5.199",
        }
        result = await api_VK_client.make_request("wall.getReposts", params)
        logging.info("посмотрел репостеров")
        return [user["from_id"] for user in result["response"]["items"]]

    @staticmethod
    async def get_user_ids_by_comment(
        owner_id: str, post_id: str, count: int = 100, vk_token=VK_TOKEN
    ) -> list[int]:
        """

        Возращает список айди пользователей,
        которые комментировали  пост Вконтанке
        """
        params = {
            "owner_id": owner_id,
            "post_id": post_id,
            "access_token": vk_token,
            "v": "5.199",
            "count": count,
        }
        result = await api_VK_client.make_request("wall.getComments", params)
        logging.info("посмотрел комментаторов")
        return [user["from_id"] for user in result["response"]["items"]]

    @staticmethod
    async def check_subscriber(group_id, user_ids, vk_token=VK_TOKEN):
        """
        Проверяет, является ли пользователи подписчиком группы или нет
        """
        params = {
            "group_id": group_id,
            "user_ids": ",".join(map(str, user_ids)),
            "access_token": vk_token,
            "v": "5.199",
        }
        res = await api_VK_client.make_request("groups.isMember", params)
        logging.info(f"Проверка подписчиков")
        return [user["user_id"] for user in res["response"] if user["member"] == 1]

    @staticmethod
    async def get_user_info_by_id(
        user_ids: List[int], vk_token=VK_TOKEN
    ) -> List[Winner]:
        """
        Возращает Имю и Фамилию пользователя по его айди
        """
        params = {
            "user_ids": ",".join(map(str, user_ids)),
            "fields": "first_name,last_name",  # указываем поля которые хотим получить из ответа
            "access_token": vk_token,
            "v": "5.199",
        }
        result = await api_VK_client.make_request("users.get", params)
        logging.info("получил информацию о подписчиках группы")
        list_winer = [
            Winner(
                first_name=user["first_name"],
                last_name=user["last_name"],
                profile_url=f"https://vk.com/id{user['id']}",
            )
            for user in result["response"]
        ]
        return list_winer
