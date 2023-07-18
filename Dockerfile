FROM python:3.9-slim-bookworm

RUN apt-get update && apt-get install build-essential curl git gcc python3-pip -y && rm -rf /var/lib/apt/lists/*
ADD . /news-please-ng
WORKDIR  /news-please-ng

RUN pip3 install --upgrade pip && pip3 install . --prefer-binary

CMD ["python3", " __main__.py", "-c", "/news-please-ng-config"]