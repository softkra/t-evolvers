FROM python:3

ENV PYTHONUNBUFFERED=1
ENV C_FORCE_ROOT=1
ENV DJANGODIR=/backend

RUN mkdir $DJANGODIR
WORKDIR $DJANGODIR

COPY requirements.txt $DJANGODIR/
RUN pip3 install -r requirements.txt

COPY . $DJANGODIR/

RUN apt-get update && apt-get install -y gettext 