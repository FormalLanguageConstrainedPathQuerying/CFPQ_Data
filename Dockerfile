FROM ubuntu:latest

RUN apt-get -y update && \
    apt-get -y install && \
    python3-pip

COPY . /CFPQ_Data

WORKDIR /CFPQ_Data
RUN pip3 install -r requirements.txt
