FROM ubuntu:latest

WORKDIR /taixTracking

RUN apt-get update
RUN apt-get install -y python3 python3-pip tini
RUN pip3 install tzdata --upgrade

COPY . .
RUN pip3 install -r requirements.txt
RUN playwright install
RUN playwright install-deps

RUN rm -r .github .gitignore Dockerfile LICENSE README.md requirements.txt

EXPOSE 8000/tcp
ENTRYPOINT [ "tini", "--" ]
CMD python3 /taixTracking/manage.py migrate; python3 /taixTracking/manage.py runserver 0.0.0.0:8000