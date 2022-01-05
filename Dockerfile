FROM python:3.10-alpine

WORKDIR /usr/app
COPY ./ /usr/app

RUN apk update && apk add g++ musl-dev
RUN pip3 install -r req.txt
RUN python3 manager.py setup

CMD ["python3", "manager.py", "runserver"]
