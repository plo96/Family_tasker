FROM python:3.12

RUN mkdir /src

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install poetry
ADD D:/PyCharm/Python_Projects/FamilyTasker/pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi --no-dev

EXPOSE 8000

# COPY src/. .
COPY . .

CMD gunicorn Server_fastapi:app --workers 4 --workers-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000


# COPY requirements.txt .
#
# RUN pip install -r requirements.txt
#
# RUN chmod a+x docker/*.sh
#
# COPY . .

# WORKDIR src
