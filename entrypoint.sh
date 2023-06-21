#!/bin/sh

export FLASK_DEBUG=1
export FLASK_APP=musicapi.app

flask db init
flask db migrate
flask db upgrade
flask run --host=0.0.0.0
