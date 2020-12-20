FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc musl-dev libffi-dev mc

WORKDIR /theater-api

ADD . /theater-api

RUN pip install -r requirements.txt

CMD gunicorn -c app/configs.py server:app
