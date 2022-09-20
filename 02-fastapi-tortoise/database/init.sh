#!/bin/bash

psql -U postgres -d starwars -a -f /app/scripts/db/seed.sql
