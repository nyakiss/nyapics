nyapics
#########

nyapics is a image uploader written in Python using Flask

Example installation
--------------------
::

    cd /var/www
    git clone git://github.com/nyakiss/nyapics.git
    cd nyapics
    virtualenv pyenv
    source pyenv/bin/activate
    pip install -r requirements.txt
    python manage.py createinstance
    nano instance/settings.cfg
    python manage.py createdb

nginx config
------------
::

    server {
        server_name example.com;

        location = /favicon.ico {
            root /var/www/nyapics/nyapics/static;
        }
        location /images {
            root /var/www/nyapics/instance;
        }
        location /thumbnails {
            root /var/www/nyapics/instance;
        }
        location /static {
            root /var/www/nyapics/nyapics;
        }
        location / {
            include uwsgi_params;
            uwsgi_pass 127.0.0.1:3030;
        }
    }

uWSGI config
------------
::

    [uwsgi]
    chdir = /var/www/nyapics
    pythonpath = /var/www/nyapics
    virtualenv = /var/www/nyapics/pyenv
    module = application
    touch-reload = /var/www/nyapics/instance/settings.cfg
    socket = 127.0.0.1:3030
    processes = 2

