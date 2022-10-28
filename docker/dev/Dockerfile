FROM ubuntu:22.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt update && apt install -y \
    python3-pip
RUN pip install --upgrade pip
RUN pip install poetry

ADD . /app
WORKDIR /app

RUN poetry install

EXPOSE 5000

COPY ./docker/docker-entrypoint.sh /

ENV PYTHONPATH /app
ENTRYPOINT ["/docker-entrypoint.sh"]
