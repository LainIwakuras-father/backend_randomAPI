FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_VIRTUALENVS_CREATE=false

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --only main --no-root --no-interaction --no-ansi

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

# CMD ["python", "main.py"]