FROM python:3.6-alpine

RUN adduser -D azurerct

WORKDIR /home/azurerct

COPY requirements.txt requirements.txt
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY mainPage.py config.py boot.sh ./
COPY tcl tcl

RUN chmod a+x boot.sh

ENV FLASK_APP mainPage.py

RUN chown -R azurerct:azurerct ./
USER azurerct

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]