FROM python:3.7

WORKDIR /server
COPY server /server
ADD requirements.txt requirements.txt
ADD consumer/consumer.py consumer.py
ADD entrypoint.sh entrypoint.sh
RUN chmod a+x entrypoint.sh
RUN python -m pip install -r requirements.txt

ENV DJANGO_SUPERUSER_EMAIL=admin@hackorama.com \
    DJANGO_SUPERUSER_PASSWORD=admin \
    DJANGO_SUPERUSER_USERNAME=admin

EXPOSE 8000

ENTRYPOINT [ "/server/entrypoint.sh" ]
