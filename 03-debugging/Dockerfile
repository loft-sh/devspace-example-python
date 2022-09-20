FROM python:3.10.7-slim-bullseye

WORKDIR /client

COPY . .

RUN pip install --no-cache-dir --upgrade .

ENTRYPOINT ["client"]
