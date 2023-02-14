FROM python:3.10-alpine
RUN apk update \
    && apk add libpq postgresql-dev \
    && apk add build-base
COPY ./requirements.txt /app/requirements.txt
COPY ./entrypoint.sh /app/entrypoint.sh
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
CMD ["./entrypoint.sh"]
