import aiohttp
import logging
from utils.exceptions import VKAPIError

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

            
            