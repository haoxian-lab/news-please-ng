FROM python:3.9-alpine3.17

RUN apk add -U --no-cache build-base curl git make gcc python3-dev libffi-dev musl-dev libxml2-dev libxslt-dev openssl-dev zlib-dev jpeg-dev
ADD . /news-please-ng
WORKDIR  /news-please-ng

RUN pip3 install .

CMD ["python3", " __main__.py", "-c", "/news-please-ng-config"]