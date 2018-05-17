FROM ubuntu:17.10

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV YETI_WEB_LISTEN_INTERFACE 0.0.0.0

RUN apt-get update && apt-get install -y \
    npm \
    python3-pip
RUN pip3 install pipenv
ADD . /opt/yeti
WORKDIR /opt/yeti/yeti/web/frontend
RUN npm install && npm run build
WORKDIR /opt/yeti
RUN pipenv install --system --deploy

EXPOSE 5000

COPY ./docker/docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["webserver"]
