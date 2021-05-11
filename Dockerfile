FROM python:latest

COPY . /CFPQ_Data

WORKDIR /CFPQ_Data
RUN pip3 install -r requirements.txt
