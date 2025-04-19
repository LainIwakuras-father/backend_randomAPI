# Raffle Backend API

Backend для рандомайзера конкурсов с интеграцией VK API и Telegram Web Apps.

## Основные функции
- Создание и управление розыгрышами
- Проверка подписок на группы через VK API
- Генерация уникальных победителей
- Интеграция с Telegram Web Apps (другой мой репозиторий)
- Хранение истории розыгрышей

## Технологии
- **Python 3.12**
- **FastAPI** - веб-фреймворк
- **Docker** - контейнеризация
- **VK API** - проверка подписок

## Требования
- Python 
- Docker и Docker Compose (опционально)

## Быстрый старт
```bash
    git clone https://github.com/LainIwakuras-father/backend_randomAPI.git
    cd backend_randomAPI
    python main.py
```
## Настройка окружения
Создайте .env файл:
в нем должен быть VK TOKEN сервисного приложения,получить его можно здесь [text](https://dev.vk.com/ru).
И Домен для Телеграм мини приложение (если вы разрабатываете TG MINI APPS) 


## Docker
```bash
docker build -t random-api .
docker run -p 8000:8000 --env-file .env random-api
```

## Документация API
Документация для API находится по ссылке когда вы у себя запустите приложение [text](http://localhost:8000/docs)

Endpoints: POST /get_winners , POST /get_reroll

Запрос к /get_winners (пример с значениями по умолчанию):
```
{
    post_url: HttpUrl
    raffle_name: Optional[str] = None
    criteria: {
        likes: bool = False
        reposts: bool = False
        comments: bool = False 
    }
    required_groups: List[HttpUrl] = []
    check_own_group: bool = False
    count_winners: int 
}

```

Запрос к /get_reroll (пример с значениями по умолчанию):
```
{
   current_winners: List[
    {
        url:HttpUrl
        first_name:str
        last_name:str
        id:int
    },
   ] # Текущий список победителей
   winner_to_reroll_id: int # ID пользователя, которого перевыбираем
}

```