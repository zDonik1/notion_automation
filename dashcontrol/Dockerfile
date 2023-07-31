FROM python:3.11-alpine

WORKDIR /dashcontrol

RUN apk update && apk upgrade --available && sync
RUN pip install --upgrade pip

COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0", "--access-logfile=-", "dashcontrol:app"]