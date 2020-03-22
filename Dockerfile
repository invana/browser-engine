FROM python:3.6
MAINTAINER Ravi RT Merugu <ravi@invanalabs.ai>
ENV PYTHONUNBUFFERED 1

ARG auth_token
ARG selenium_host
ARG browser_type
ENV AUTH_TOKEN ${auth_token}
ENV DEFAULT_SELENIUM_HOST ${selenium_host}
ENV DEFAULT_BROWSER_TYPE ${browser_type}

RUN [ -d /app ] || mkdir /app;
COPY  ./ /app
WORKDIR /app

RUN pip install -r requirements.txt
EXPOSE 5000
CMD uwsgi --socket 0.0.0.0:5000 --protocol=http -w browser_engine.server.wsgi:application --processes 4 --threads 2