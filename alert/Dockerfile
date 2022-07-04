FROM python:3

ENV ALERTDIR=/alert

RUN mkdir $ALERTDIR
WORKDIR $ALERTDIR
RUN pip install redis
RUN pip install requests
COPY . $ALERTDIR/
