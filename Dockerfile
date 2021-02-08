FROM ubuntu:18.04

COPY . /CFPQ_Data

WORKDIR /CFPQ_Data
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip3 install -r requirements.txt
