FROM python:3.11-alpine

WORKDIR /new_week

RUN apk update && apk upgrade --available && sync
RUN pip install --upgrade pip

COPY . .
RUN pip install -r requirements.txt

ADD cron_new_week /etc/cron.d/cron_new_week
RUN chmod 0644 /etc/cron.d/cron_new_week
RUN crontab /etc/cron.d/cron_new_week

ENTRYPOINT ["crond", "-f"]