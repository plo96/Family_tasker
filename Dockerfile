FROM python:3.12

RUN mkdir /app

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install poetry
COPY pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi --only main

EXPOSE 8000

COPY migrations/. migrations/.
COPY alembic.ini .
COPY src/. src/.
COPY .env .
