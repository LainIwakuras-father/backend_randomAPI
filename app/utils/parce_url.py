import re

def  parse_vk_url(url):
    '''
    Парсит ссылку на пост ВКонтакте и возвращает айди сообщества и айди поста.
    '''
    match_post= re.search(r'wall(-?\d+)_(\d+)', url)
    if match_post:
         group_id, item_id = match_post.groups()
         return group_id, item_id
    raise ValueError(f"Unsupported VK URL format: {url}")

