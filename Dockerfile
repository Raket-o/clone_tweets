# Dockerfile

FROM python:3.10

COPY ./requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY ./config_data ./config_data
COPY alembic.ini alembic.ini
COPY alembic alembic
COPY .env .env
COPY ./app ./app

EXPOSE 8000

ENTRYPOINT ["./app/docker-entrypoint.sh"]
