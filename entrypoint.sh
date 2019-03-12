#!/bin/bash
cd /var/www/oidc
if [[ $SEED_DB == "True" ]]; then
	/usr/local/bin/python /var/www/oidc/manage.py makemigrations && /usr/local/bin/python /var/www/oidc/manage.py migrate && /usr/local/bin/python /var/www/oidc/manage.py creatersakey
fi
if [[ $SEED_DB == "False" ]]; then
	/usr/local/bin/python /var/www/oidc/manage.py makemigrations && /usr/local/bin/python /var/www/oidc/manage.py migrate && /usr/local/bin/gunicorn --config /var/www/oidc/deploy/gunicorn.conf --log-config /var/www/oidc/deploy/logging.conf provider_app.wsgi:application
fi
exit