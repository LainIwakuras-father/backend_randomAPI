
import logging
import asyncio
import aiohttp
import re
import os
from dotenv import load_dotenv
# from app.config import VK_TOKEN

#ID СООБЩЕСТВА очень важен минус в начале или название 
load_dotenv()
## использовать либо тот либо тот токен для работы с группой и пользователями
VK_TOKEN = os.getenv('VK_TOKEN','')
owner_id = "-228217476"
group_screen_name = "byskaza"
user_ids = set()
#https://vk.com/wall-228217476_68 вот такую ссылку надо парсить
# перенеси в другой файл по хорошему!
def  parse_vk_url(url):
    '''
    Парсит ссылку на пост ВКонтакте и возвращает айди сообщества и айди поста.
    '''
    match_post= re.search(r'wall(-?\d+)_(\d+)', url)
    if match_post:
         group_id, item_id = match_post.groups()
         return int(group_id), int(item_id)
    raise ValueError(f"Unsupported VK URL format: {url}")



async def get_club_by_id():
    """
    Возвращает айди группы по её ссылке
    """
    group_screen_name = "byskaza"

    params = {
        'group_id': group_screen_name,
        "access_token": VK_TOKEN,
        "v": "5.199",
        
    }
    async with aiohttp.ClientSession() as session:
            async with session.get('https://api.vk.com/method/groups.getById', params=params) as response:
                result = await response.json()
                logging.info(f"Response from VK API: {result}")
                return result
        
        
async def get_user_ids_by_likes():
    """
    Возращает список айди пользователей, 
    которые лайкнули, комментировали, репостнули  пост Вконтанке
    """
    #надо сделать логику парсинга ссылки на пост и присваивать айди вводимым аргументом функции
    # 'group_id': group_screen_name,  'owner_id': owner_id,
    #owner_id и items_id это айди сообщества и айди поста соответственно так как от пользователя мы получаем ссылку на пост мы их тока парсим из URL
    params = {
        'type': 'post',
        "owner_id": owner_id,
        'item_id': "68",
        "access_token": VK_TOKEN,
        "v": "5.199",
        
    }
    
    async with aiohttp.ClientSession() as session:
            
            async with session.get('https://api.vk.com/method/likes.getList', params=params) as response:
                result = await response.json()
                user_ids.update(result['response']['items'])
                return user_ids
            
         
async def get_user_ids_by_repost():
    """
    Возращает список айди пользователей, 
    которые лайкнули, комментировали, репостнули  пост Вконтанке
    """
    #надо сделать логику парсинга ссылки на пост и присваивать айди вводимым аргументом функции
    # 'group_id': group_screen_name,  'owner_id': owner_id,
    #owner_id и items_id это айди сообщества и айди поста соответственно так как от пользователя мы получаем ссылку на пост мы их тока парсим из URL
    params = {
        "owner_id": owner_id,
        'post_id': "68",
        "access_token": VK_TOKEN,
        "v": "5.199",
    }
    
    async with aiohttp.ClientSession() as session:
            
            async with session.get('https://api.vk.com/method/wall.getReposts', params=params) as response:
                result = await response.json()
                return [user['from_id'] for user in result['response']['items']]
            
         

async def get_user_ids_by_comment():
    """
    Возращает список айди пользователей, 
    которые лайкнули, комментировали, репостнули  пост Вконтанке
    """
    #надо сделать логику парсинга ссылки на пост и присваивать айди вводимым аргументом функции
    # 'group_id': group_screen_name,  'owner_id': owner_id,
    #owner_id и items_id это айди сообщества и айди поста соответственно так как от пользователя мы получаем ссылку на пост мы их тока парсим из URL
    params = {
        "owner_id": owner_id,
        'post_id': "68",
        "access_token": VK_TOKEN,
        "v": "5.199",
        'count': '100',
    }
    
    async with aiohttp.ClientSession() as session:
            
            async with session.get('https://api.vk.com/method/wall.getComments', params=params) as response:
                result = await response.json()
                
                return [user['from_id'] for user in result['response']['items']]
            
              

async def check_subscriber():
    '''
    Проверяет, является ли пользователь подписчиком группы или нет 
    '''
    pass

async def get_user_info_by_id():
    """
    Возращает Имю и Фамилию пользователя по его айди
    """
    pass


#testing
async def main():
    logging.basicConfig(level=logging.INFO)
    logging.info('ЗАПУСКАЮ...')
    url = "https://vk.com/wall-228217"
    group_id, owner_id = parse_vk_url(url)
    logging.info(f"Айди сообщества: {group_id} айди поста: {owner_id}")
    likes = await get_user_ids_by_likes()
    logging.info(f"Пользователи, которые лайкнули пост: {likes}")
    reposts = await get_user_ids_by_repost()
    logging.info(f"Пользователи, которые репостнули пост: {reposts}")
    comments = await get_user_ids_by_comment()
    logging.info(f"Пользователи, которые оставили комментарий посту: {comments}")

if __name__ == '__main__':
    asyncio.run(main())

