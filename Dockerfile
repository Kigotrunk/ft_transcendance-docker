from debian:buster

RUN apt update -y
RUN apt upgrade -y
RUN apt install python3 -y
#RUN apt install python3.11-venv -y
RUN apt install python-pip -y
RUN apt-get install postgresql-server-dev-all -y

COPY new/requirement.txt .
#RUN pip install -r requirement.txt

#RUN sudo -u postgres psql
#RUN CREATE DATABASE "new";
#RUN \password