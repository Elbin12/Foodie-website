
FROM python:3.12.3

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib \
    && apt-get clean

RUN mkdir /docker_foodstore/

WORKDIR /docker_foodstore

COPY . /docker_foodstore/

RUN pip install -r requirement.txt

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
