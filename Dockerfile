FROM python:3.12.3

# Set the working directory in the container
WORKDIR /usr/src/app

# Define environment variable
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# RUN apt-get update && apt-get install -y python3-opencv
# RUN pip install opencv-python