FROM ubuntu:latest

RUN apt -y update && \
    apt-get -y install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt -y install \
    python3.9 \
    python3-pip \
    git \
    openjdk-8-jdk

COPY . /CFPQ_Data

WORKDIR /CFPQ_Data
RUN pip3 install -r requirements.txt
