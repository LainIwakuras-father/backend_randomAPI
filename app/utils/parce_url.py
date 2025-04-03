import re




class VKUrlParser:
     @staticmethod
     def  parse_vk_post(url:str) -> tuple[int]:
          '''
          Парсит ссылку на пост ВКонтакте и возвращает кортеж айди сообщества и айди поста.
          '''
          
          match_post= re.search(r'wall(-?\d+)_(\d+)', url)
          if match_post:
               group_id, item_id = match_post.groups()
               return group_id, item_id
          raise ValueError(f"Unsupported VK URL format: {url}")
     
     @staticmethod
     def parse_vk_groups(urls):
          pattern = r'^(?:https?://)?vk.com/(?:club)?([a-zA-Z0-9_]+)'
          for url in urls:
               match = re.match(pattern, url)
               if match:
                    group_name = match.group(1)
                    yield group_name
               else:
                    raise ValueError(f"Unsupported VK URL format: {url}")
               



