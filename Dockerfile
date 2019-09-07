FROM python:3.7-slim-buster

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /appFlask/requirements.txt
COPY . /appFlask

WORKDIR /appFlask

RUN pip install -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000

RUN ["ls" ]

#WORKDIR /app/app

#RUN ["ls" ]
ENTRYPOINT [ "bash", "./boot.sh" ]
