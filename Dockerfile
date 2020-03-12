# pull official base image
FROM python:3.8.1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY ./requirements.txt /usr/src/app/
RUN pip install -r requirements.txt

COPY ./ /usr/src/app/
