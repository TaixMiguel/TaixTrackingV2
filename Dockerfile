FROM ubuntu:latest

WORKDIR /taixTracking
EXPOSE 8000/tcp

RUN apt-get update && \
    apt-get install -y python3 python3-pip tini && \
    pip3 install tzdata --upgrade

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN playwright install && \
    playwright install-deps

COPY . .
RUN chmod 777 /taixTracking/entrypoint.sh

ENTRYPOINT [ "tini", "--" ]
CMD /taixTracking/entrypoint.sh