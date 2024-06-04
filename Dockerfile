FROM python:3.12.3

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# RUN apt-get update && apt-get install -y python3-opencv
# RUN pip install opencv-python