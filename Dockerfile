FROM python:3-alpine

RUN apk add --no-cache postgresql-client

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN apk add --no-cache -t .devtools postgresql-dev gcc python3-dev musl-dev  && pip install -r requirements.txt && apk del --no-cache .devtools
COPY . .

EXPOSE 8000
CMD ["sh", "./startup.sh"]
