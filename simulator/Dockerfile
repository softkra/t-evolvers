FROM python:3

ENV SIMULATORDIR=/simulator

RUN mkdir $SIMULATORDIR
WORKDIR $SIMULATORDIR
#RUN python main.py
RUN pip install redis
COPY . $SIMULATORDIR/
