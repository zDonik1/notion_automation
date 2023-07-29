FROM python:3.11-alpine

WORKDIR /cron

RUN apk update && apk upgrade --available && sync

COPY . .
RUN pip install -r requirements.txt

ADD cron_new_week /etc/cron.d/cron_new_week
RUN chmod 0644 /etc/cron.d/cron_new_week
RUN crontab /etc/cron.d/cron_new_week

ENTRYPOINT ["crond", "-f"]