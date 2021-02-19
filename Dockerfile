FROM ubuntu:latest

RUN apt -y update && \
    apt-get install software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install -y \
    python3.9 \
    python3-pip \
    git \
    default-jre \
    default-jdk

COPY . /CFPQ_Data

WORKDIR /CFPQ_Data
RUN pip3 install -r requirements.txt
