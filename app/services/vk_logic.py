
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
owner_ids = "228217476" #для is.Member нужно без минуса
item_id = "38"
group_screen_name = "byskaza"
user_ids = set()

#https://vk.com/wall-228217476_68  https://vk.com/wall-228217476_38вот такую ссылку надо парсить
# перенеси в другой файл по хорошему!


class VKAPIError(Exception):
    """Custom exception for VK API errors."""
    pass



def  parse_vk_url(url):
    '''
    Парсит ссылку на пост ВКонтакте и возвращает айди сообщества и айди поста.
    '''
    match_post= re.search(r'wall(-?\d+)_(\d+)', url)
    if match_post:
         group_id, item_id = match_post.groups()
         return int(group_id), int(item_id)
    raise ValueError(f"Unsupported VK URL format: {url}")



class api_VK_client:
     
    @staticmethod    
    async def make_request(method, params):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f'https://api.vk.com/method/{method}', params=params) as response:
                    result = await response.json()
                    if 'error' in result:
                        error_code = result['error']['error_code']
                        error_msg = result['error']['error_msg']
                        raise VKAPIError(f'VK API Error ({error_code}): {error_msg}')
                    return result
            except aiohttp.ClientError as e:
                logging.error(f"Сетевая ошибка при запросе API ВКонтакте:: {e}")
                raise VKAPIError(f"Сетевая ошибка при запросе API ВКонтакте:: {e}")

            
            

    @staticmethod
    async def get_club_by_id(group_screen_name , vk_token = VK_TOKEN):
        """
        Возвращает айди группы по её ссылке c названием
        """
        params = {
            'group_id': group_screen_name,
            "access_token": vk_token,
            "v": "5.199",
            
        }

        res =  await api_VK_client.make_request("groups.getById",params)
        return res['response']['groups'][0]['id']



    @staticmethod
    async def get_user_ids_by_likes(owner_id,item_id, vk_token = VK_TOKEN):
        """
        Возращает список айди пользователей, 
        которые лайкнули  пост Вконтанке
        """
        params = {
            'type': 'post',
            "owner_id": owner_id,
            'item_id': item_id,
            "access_token": vk_token,
            "v": "5.199",
            
        }
        
        result = await api_VK_client.make_request("likes.getList",params)
        return result['response']['items']




        
        

            
    @staticmethod      
    async def get_user_ids_by_repost(owner_id,post_id,vk_token=VK_TOKEN):
        """
        Возращает список айди пользователей, 
        которые репостнули  пост Вконтанке
        """
        params = {
            "owner_id": owner_id,
            'post_id': post_id,
            "access_token": vk_token,
            "v": "5.199",
        }
        result = await api_VK_client.make_request("wall.getReposts",params)
        return [user['from_id'] for user in result['response']['items']]
            
         
    @staticmethod
    async def get_user_ids_by_comment(owner_id,post_id,count,vk_token=VK_TOKEN):
        """
        Возращает список айди пользователей, 
        которые комментировали  пост Вконтанке
        """
        #надо сделать логику парсинга ссылки на пост и присваивать айди вводимым аргументом функции
        # 'group_id': group_screen_name,  'owner_id': owner_id,
        #owner_id и items_id это айди сообщества и айди поста соответственно так как от пользователя мы получаем ссылку на пост мы их тока парсим из URL
        params = {
            "owner_id": owner_id,
            'post_id': post_id,
            "access_token": vk_token,
            "v": "5.199",
            'count': count,
        }
        result = await api_VK_client.make_request("wall.getComments",params)
                    
        return [user['from_id'] for user in result['response']['items']]
            
              
    @staticmethod
    async def check_subscriber(group_id,user_ids,vk_token=VK_TOKEN):
        '''
        Проверяет, является ли пользователь подписчиком группы или нет 
        '''
        params = {
            'group_id': group_id,
            'user_ids': ','.join(map(str, user_ids)), # преобразование списка в строку через запятую !!!! оказыается
            "access_token": vk_token,
            "v": "5.199",
        }
        res = await api_VK_client.make_request("groups.isMember",params)
        return [user['user_id'] for user in res['response'] if user['member'] == 1]
    
    
    @staticmethod     
    async def get_user_info_by_id():
        """
        Возращает Имю и Фамилию пользователя по его айди
        """
        pass


#testing
async def main():
    logging.basicConfig(level=logging.INFO,)
    logging.info('ЗАПУСКАЮ...')
    likers = await api_VK_client.get_user_ids_by_likes(owner_id,item_id)
    logging.info(f'Лайкнули пост: {likers}')
    checker = await api_VK_client.check_subscriber(owner_ids,likers)
    logging.info(f'Подписчики группы из лайкнувших пост: {checker}')

if __name__ == '__main__':
    asyncio.run(main())

