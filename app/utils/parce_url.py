import re




class VKUrlParser:
     @staticmethod
     def  parse_vk_post(url):
          '''
          Парсит ссылку на пост ВКонтакте и возвращает айди сообщества и айди поста.
          '''
          match_post= re.search(r'wall(-?\d+)_(\d+)', url)
          if match_post:
               group_id, item_id = match_post.groups()
               return group_id, item_id
          raise ValueError(f"Unsupported VK URL format: {url}")
     
     @staticmethod
     def parse_vk_groups(urls):
          for url in urls:
               match = re.search(r'club([^/]+)', url)
               if match:
                    group_name = match.group(1)
                    yield group_name
               else:
                    raise ValueError(f"Unsupported VK URL format: {url}")