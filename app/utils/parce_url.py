import re

from pydantic import HttpUrl


class VKUrlParser:
    @staticmethod
    def parse_vk_post(url: HttpUrl) -> tuple[int]:
        """
        Парсит ссылку на пост ВКонтакте и возвращает кортеж айди сообщества и айди поста.
        """
        match_post = re.search(r"wall(-?\d+)_(\d+)", str(url))
        if match_post:
            group_id, item_id = match_post.groups()
            return group_id, item_id
        raise ValueError(f"Unsupported VK URL format: {url}")

    @staticmethod
    def parse_vk_groups(url: HttpUrl):
        pattern = r"^(?:https?://)?vk.com/(?:club)?([a-zA-Z0-9_]+)"
        # for url in urls:
        match = re.match(pattern, str(url))
        if match:
                group_name = match.group(1)
                return group_name
        else:
                raise ValueError(f"Unsupported VK URL format: {url}")
