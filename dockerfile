FROM tiangolo/uwsgi-nginx-flask:python3.6

RUN mkdir app
WORKDIR /app

COPY ./app/ /app
RUN pip install -r requirements.txt

