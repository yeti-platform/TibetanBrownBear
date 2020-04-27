FROM ubuntu:18.04

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get install -y \
    python3-pip \
    python-yara \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install pipenv
ADD . /app
WORKDIR /app
RUN pipenv install --system --deploy

EXPOSE 5000

COPY ./docker/docker-entrypoint.sh /
ENV PYTHONPATH /app
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["webserver"]
