FROM python:3.7

# DATA=sample-data        : will use 'localhost' for consumer whcih is the default
# DATA=sample-data-docker : will use 'consumer' the service name used used in docker compose
ENV DATA=sample-data \
    DJANGO_SUPERUSER_EMAIL=admin@hackorama.com \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_USERNAME=admin

WORKDIR /server

COPY server /server
ADD requirements.txt requirements.txt
ADD consumer/consumer.py consumer.py
ADD entrypoint.sh entrypoint.sh

RUN chmod a+x entrypoint.sh
RUN python -m pip install -r requirements.txt

# Exposing 8888 in case of running a dev consumer in the same container
EXPOSE 8000 8888

ENTRYPOINT [ "/server/entrypoint.sh" ]
