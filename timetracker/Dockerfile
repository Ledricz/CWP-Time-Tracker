FROM  python:3.10.12

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./manage-django.sh .

ENV PYTHONUNBUFFERED=1

COPY . /time-tracker
WORKDIR /time-tracker

EXPOSE 8000