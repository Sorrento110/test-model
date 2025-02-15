FROM python:3.9.2

RUN pip install --upgrade pip

COPY . /model
WORKDIR /model

RUN pip install -r requirements.txt

