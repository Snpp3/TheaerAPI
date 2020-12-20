FROM python:3.7-alpine

RUN apk update && apk add postgresql-dev gcc musl-dev libffi-dev mc

WORKDIR /theater-api

ADD . /theater-api

# Salary and premium cron every month
RUN echo '* * * * * /usr/local/bin/python /theater-api/cronjob_run.py salary_payment_run' >> /etc/crontabs/root

RUN pip install -r requirements.txt

CMD crond & gunicorn -c app/configs.py server:app
