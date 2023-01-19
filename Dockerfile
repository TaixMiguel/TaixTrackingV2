FROM alpine:latest

WORKDIR /taixTracking

RUN apk add --no-cache python3 py3-pip tini; \
    pip install --upgrade pip setuptools-scm; \
    pip install pytz --upgrade; \
    pip install tzdata --upgrade;

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY TaixTracking TaixTracking
COPY tracking tracking
COPY manage.py manage.py

EXPOSE 8000/tcp
ENTRYPOINT [ "tini", "--" ]
CMD python3 /taixTracking/manage.py migrate; python3 /taixTracking/manage.py runserver 0.0.0.0:8000