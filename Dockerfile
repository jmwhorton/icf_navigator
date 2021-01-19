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
COPY prod-requirements.txt .
RUN pip install -r prod-requirements.txt

RUN pip install gunicorn

COPY icf_navigator ./icf_navigator

WORKDIR /code/icf_navigator

RUN yarn install
RUN yarn build
RUN rm -rf node_modules
RUN apk del yarn nodejs

ARG ICF_DJANGO_SECRET_KEY
ENV ICF_DJANGO_SECRET_KEY=$ICF_DJANGO_SECRET_KEY
ARG ICF_DATABASE_USER
ENV ICF_DATABASE_USER=$ICF_DATABASE_USER
ARG ICF_DATABASE_PASSWORD
ENV ICF_DATABASE_PASSWORD=$ICF_DATABASE_PASSWORD
ARG ICF_DATABASE_HOST
ENV ICF_DATABASE_HOST=$ICF_DATABASE_HOST

ENV DJANGO_SETTINGS_MODULE=icf_navigator.prod_settings
ENTRYPOINT ["gunicorn"]
CMD ["icf_navigator.wsgi", "--bind=127.0.0.1:3000", "--workers=2"]
