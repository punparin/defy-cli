FROM ubuntu:18.04

RUN apt-get update \
    && apt-get install -y python3-pip python3-dev \
    && cd /usr/local/bin \
    && ln -s /usr/bin/python3 python \
    && pip3 install --upgrade pip

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY . /defy

WORKDIR /defy

RUN python setup.py sdist \
    && pip3 install dist/defy-0.0.0.tar.gz

ENTRYPOINT ["defy", "all"]