FROM python:3.8.9

LABEL maintainer="inhun321@khu.ac.kr"

COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . /usr/src/app

ENTRYPOINT ["python3", "main.py"]