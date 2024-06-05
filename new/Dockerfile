FROM debian:buster

RUN apt update -y && apt upgrade -y
RUN apt install build-essential libssl-dev libffi-dev libpq-dev python-dev -y
RUN apt install python3.11 python3-pip -y
RUN python3 -m pip install --upgrade pip

WORKDIR ./app
COPY . ./app
RUN python3 -m pip install requests Pillow django daphne django-cors-headers django-allauth djangorestframework djangorestframework-simplejwt psycopg2-binary channels

EXPOSE 8000

RUN chmod +x ./app/setup.sh

CMD ["sh", "./app/setup.sh"]
