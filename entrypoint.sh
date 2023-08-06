#!/usr/bin/env bash

export FLASK_APP=musicapi.app

chmod +x wait-for-it.sh
./wait-for-it.sh db:5432 -t 600000000 -- echo "postgresql is up"

flask db upgrade
flask run --host=0.0.0.0
