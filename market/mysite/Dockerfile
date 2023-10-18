FROM python:3.9.6
ENV PYTHONUNBUFFERED 1 
RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /srv/market
ADD . /srv/market

WORKDIR /srv/market

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"] # 실행