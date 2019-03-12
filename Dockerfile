FROM python:3.7-slim

COPY . /var/www/oidc

RUN apt-get update \
    # Install libs apt
    && apt-get -y install default-libmysqlclient-dev build-essential git curl wget gzip --no-install-recommends \
    # Install libs python
    && mkdir /var/www/oidc/provider_app/geoip \
    && cd /var/www/oidc/provider_app/geoip \
    && wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-City.tar.gz \
    && wget https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz \
    && tar xvzf GeoLite2-City.tar.gz \
    && tar xvzf GeoLite2-Country.tar.gz \
    && mv GeoLite2-Country_*/*.mmdb GeoLite2-City_*/*.mmdb /var/www/oidc/provider_app/geoip \
    && rm -rf /var/www/oidc/provider_app/geoip/GeoLite2-*_* /var/www/oidc/provider_app/geoip/*.tar.gz \
    && cd /var/www/oidc \
    && pip install -r requirements.txt \
    && pip install -U --force-reinstall --no-binary :all: gevent \
    && rm -rf requirements.txt README.md Dockerfile gitlab-ci.yml \
    # Reduce image size
    && apt-get remove --purge -y build-essential git curl wget gzip --allow-remove-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && apt-get autoclean \
    && apt-get autoremove -y \
    && rm -rf /var/cache/debconf/*-old \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc/* /usr/share/locale/* \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/cache/apt/archives/*.deb /var/cache/apt/archives/partial/*.deb /var/cache/apt/*.bin \
    && chmod +x entrypoint.sh

ENTRYPOINT ["/var/www/oidc/entrypoint.sh"]
