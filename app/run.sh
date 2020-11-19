#!/usr/bin/env bash

check_connectivity() {
    echo 'Check if AnalEyeZer is up...'

    while ! nc -z ${ANALEYEZER_HOST} 5000; do

      sleep 0.1

    done
    echo 'AnalEyeZer is up and Running'

    echo 'Check if PostgreSQL is up...'
    while ! nc -z ${POSTGRES_HOST} 5432; do
      sleep 0.1
    done
    echo 'PostgreSQL is up and Running'
}

if [[ "$PROD_STATUS" = true ]]
then
    check_connectivity
fi


echo " Run gunicorn"
gunicorn --workers=4 -b 0.0.0.0:5000 wsgi:app --timeout 200 --reload