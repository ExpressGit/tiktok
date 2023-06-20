# This Dockerfile is used to build an Python environment
FROM python:3.9-slim-bullseye

LABEL maintainer="imgyh<admin@imgyh.com>"

WORKDIR /app

ADD . $WORKDIR

RUN sed -i s/deb.debian.org/mirrors.aliyun.com/g /etc/apt/sources.list

RUN pip3 install -r requirements_docker.txt

ENV TZ=Asia/Shanghai

# CMD ["echo", "hello world"]
