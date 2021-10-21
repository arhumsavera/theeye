FROM python:3.8

ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /theeye

# Set the working directory to /theeye
WORKDIR /theeye

# Copy the current directory contents into the container
ADD . /theeye/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt