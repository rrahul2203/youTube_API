FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY . /code/
RUN python3 -m pip install -r requirement.txt