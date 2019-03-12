
--------

Identity Provider del estado, es un sistema SSO (Single Sign On) que utiliza el protocolo OpenID Connect

Licencia
--------

Este software esta licenciado bajo la licencia GPLv2

Requerimientos
--------
* Python 3.7 https://github.com/python/cpython
* MySQL 5.7 https://github.com/mysql/mysql-server

Bibliotecas
--------

* https://github.com/python/cpython
* https://github.com/juanifioren/django-oidc-provider
* https://github.com/django/django
* https://github.com/joke2k/django-environ
* https://github.com/niwinz/django-redis
* https://github.com/PyMySQL/mysqlclient-python
* https://github.com/requests/requets
* https://github.com/ottoyiu/django-cors-headers
* https://github.com/rollbar/pyrollbar
* https://github.com/maxmind/GeoIP2-python
* https://github.com/benoitc/gunicorn
* https://github.com/gevent/gevent
* https://github.com/sebest/json-logging-py
* https://github.com/python-greenlet/greenlet

Variables de entorno
--------

* ``SITE_URL``: string, URL del sitio
* ``LOGIN_URL``: string, ruta del login
* ``SECRET_KEY``: string, se debe definir un string random
* ``DEBUG``: boolean, True para activar modo de debug
* ``CORS_ALLOW_CREDENTIALS``: boolean, activar Cors Allow Credentials
* ``CORS_ORIGIN_WHITELIST``: list, dominios separados por coma, ejemplo accounts.claveunica.gob.cl,api.claveunica.gob.cl
* ``ALLOWED_HOSTS``: list, dominios separados por comas
* ``NAME_DB``: string, nombre de la base de datos
* ``USER_DB``: string, usuario de la base de datos
* ``HOST_DB``: string, host de la base de datos
* ``PORT_DB``: int, puerto de la base de datos
* ``PASSWORD_DB``: string, password de la base de datos
* ``CACHE_LOCATION``: string, redis://host:puerto
* ``SESSION_COOKIE_AGE``: int, segundos que dura la sesion
* ``SESSION_COOKIE_DOMAIN``: string, dominio de la sesion
* ``RUNS``: list, ejemplo 99.999.999-9,88.888.888-8,55.555.555-5,44.444.444-4
* ``URL_AUTH``: string, http://host_microservicio/validateUser
* ``URL_GET_INFO_USER``: string, http://host_microservicio/userInfo
* ``TOKEN_AUTH``: string, token de los microservicios
* ``ROLLBAR_ACCESS_TOKEN``: string, access token de rollbar

variables de deploy
* ``GUNICORN_WORKERS``: int, number of workers deploy with gunicorn
* ``GUNICORN_WORKER_CLASS``: string, type of greenlet worker with gunicorn
* ``GUNICORN_ACCESSLOG``: string, error log
* ``GUNICORN_BIND``: string, ip and port to listen
* ``SEED_DB``: boolean, True para hacer poblado de la BD
* ``SANDBOX``: boolean, True para levantar ambiente sandbox
* ``PORT_UDP_LOGS``: int, puerto UDP para conectarse a microservicio de los logs

Deploy
--------

Instalar bibliotecas de Python 3.7

```
pip install -r requirements.txt
```

Realizar poblado de la BD

```
python manage.py makemigrations
python manage.py migrate
```

Crear las llaves:

```
python manage.py creatersakey
```

Iniciar aplicacion:

```
python manage.py runserver 0.0.0.0:8000
```

Deploy con Docker
--------

Realizar poblado de la BD y creación de llaves:
```
Docker run --rm -i -t git.gob.cl:4567/claveunica/oidc python manage.py makemigrations && python manage.py migrate && python manage.py creatersakey
```

Iniciar aplicacion:

```
docker run -d -i -t --env-file .env git.gob.cl:4567/claveunica/oidc
```
en el archivo .env se deben configurar las variables de entorno del sistema

Server Endpoints
--------

**/authorize endpoint**

Ejemplo de OpenID Authentication Request usando el flujo ``Authorization Code`` 

El parámetro ``scope`` es oblitagorio poner openid. 

* ``client_id=123``: Client id de la aplicación
* ``redirect_uri=http://example.com/``: URI donde retorna OpenID Connect
* ``response_type=code``
* ``scope=name run``: datos que se quieren obtener del userinfo
* ``state=abcdefgh``: string aleatorio

```curl
GET /openid/authorize?client_id=123&redirect_uri=http%3A%2F%2Fexample.com%2F&response_type=code&scope=openid%20name%20run&state=abcdefgh HTTP/1.1
Host: localhost
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded
```

Después de que el usuario inicie sesión, el servidor redirecciona a ``http://example.com/`` donde el query string ``code`` es un valor unico que pertenece a la autentificación del usuario y ``state`` es el mismo valor enviado al principio:

```curl
http://example.com/?code=5fb3b172913448acadce6b011af1e75e&state=abcdefgh
```

el parámetro ``code`` debe ser usuado para obtener el access token

**/token endpoint**

* ``client_secret``: client secret de la aplicación

```curl
POST /openid/token/ HTTP/1.1
Host: localhost
Cache-Control: no-cache
Content-Type: application/x-www-form-urlencoded
    client_id=123&client_secret=456&redirect_uri=http%253A%252F%252Fexample.com%252F&grant_type=authorization_code&code=[CODE]&state=abcdefgh
```

**/userinfo endpoint**

el parámetro ``access_token`` debe ser usuado para obtener el user info

```curl
POST /openid/userinfo/ HTTP/1.1
Host: localhost
Authorization: Bearer [ACCESS_TOKEN]
```
