FROM python:3.12

RUN mkdir /server_fastapi

WORKDIR /server_fastapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN chmod a+x docker/*.sh

COPY . .

#WORKDIR src

#CMD gunicorn Server_fastapi:app --workers 4 --workers-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
