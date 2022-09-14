FROM postgres:14.5-bullseye

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=password
ENV POSTGRES_DB=starwars

WORKDIR /app
COPY ./init.sh /docker-entrypoint-initdb.d
COPY ./seed.sql ./scripts/db/seed.sql
