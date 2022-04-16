#syntax=docker/dockerfile:1

FROM python:3.8-slim-buster
WORKDIR /app
RUN apt-get update
RUN apt-get install libsndfile1 -y
RUN apt-get install ffmpeg -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]