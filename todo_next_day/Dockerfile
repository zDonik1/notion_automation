FROM python:3.11-alpine

WORKDIR /todo_next_day

RUN apk update && apk upgrade --available && sync
RUN pip install --upgrade pip

COPY . .
RUN pip install -r requirements.txt

ADD cron_todo_next_day /etc/cron.d/cron_todo_next_day
RUN chmod 0644 /etc/cron.d/cron_todo_next_day
RUN crontab /etc/cron.d/cron_todo_next_day

ENTRYPOINT ["crond", "-f"]