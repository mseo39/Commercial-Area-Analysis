FROM python:3.9.6
ENV PYTHONUNBUFFERED 1 
RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /srv/market_front
ADD . /srv/market_front

WORKDIR /srv/market_front

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]