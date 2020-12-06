FROM python:3.8.6-alpine

RUN mkdir -p /code

WORKDIR /code

EXPOSE 3000

RUN apk update && \
    apk add --no-cache \
        gcc \
        musl-dev \
        libc-dev \
        linux-headers \
        postgresql-dev \
        nodejs \
        yarn

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install gunicorn

COPY icf_navigator ./icf_navigator

WORKDIR /code/icf_navigator

RUN yarn install
RUN yarn build
RUN rm -rf node_modules
RUN apk del yarn nodejs

ENTRYPOINT ["gunicorn"]
CMD ["icf_navigator.wsgi", "--bind=127.0.0.1:3000", "--workers=2"]
