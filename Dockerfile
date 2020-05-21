FROM python:3.7-slim

WORKDIR /opt/app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

ADD app .
EXPOSE 5000

CMD bash run.sh