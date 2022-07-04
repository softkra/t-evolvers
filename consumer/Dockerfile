FROM python:3

ENV CONSUMERDIR=/consumer

RUN mkdir $CONSUMERDIR
WORKDIR $CONSUMERDIR
RUN pip install redis
RUN pip install requests
COPY . $CONSUMERDIR/
