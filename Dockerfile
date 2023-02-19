# syntax=docker/dockerfile:1

FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY rest.py .

CMD [ "python3", "rest.py" , "--host=0.0.0.0"]
