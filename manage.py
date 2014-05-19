#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import mkdir, urandom
from os.path import join, dirname, abspath
from shutil import copy

sys.path.append(abspath(dirname(__file__)))

from flask.ext.script import Command, Option, Server, Shell, Manager
from flask.ext.script import prompt_bool
from nyapics import app


class CreateInstance(Command):

    description = "Make instance folder and copy example config to it."

    def run(self):
        INSTANCE_ROOT = app.instance_path
        for i in [
            INSTANCE_ROOT,
            join(INSTANCE_ROOT, 'images'),
            join(INSTANCE_ROOT, 'thumbnails'),
            ]:
            try:
                mkdir(i)
            except OSError:
                pass
        EXAMPLE_CONFIG = join(app.root_path, 'settings.py')
        CONFIG = join(INSTANCE_ROOT, 'settings.cfg')
        copy(EXAMPLE_CONFIG, CONFIG)
        with open(CONFIG, 'r+') as f:
            f.seek(0, 2)
            f.write("\nSECRET_KEY=%r\n" % urandom(24))
        print("Please, edit %s and then run 'manage.py createdb'" % CONFIG)


class CreateDb(Command):

    description = "Create all tables in database."

    def run(self):
        app.configure(
            SQLALCHEMY_ECHO=True,
        )
        from nyapics.models import db
        db.create_all()


class DropDb(Command):

    description = "Drop all tables in database."

    def run(self):
        if prompt_bool("Are you sure you want to lose all your data"):
            app.app.configure(
                SQLALCHEMY_ECHO=True,
            )
            from nyapics.models import db
            db.drop_all()


class CustomServer(Server):

    def handle(*args, **kwargs):
        app.configure(
            DEBUG=True,
            SQLALCHEMY_ECHO=True,
            USE_X_SENDFILE=False,
        )
        Server.handle(*args, **kwargs)


class CustomShell(Shell):

    def run(*args, **kwargs):
        app.configure(
            SQLALCHEMY_ECHO=True,
        )
        Shell.run(*args, **kwargs)


if __name__ == "__main__":
    manager = Manager(app)
    manager.add_command('createinstance', CreateInstance())
    manager.add_command('createdb', CreateDb())
    manager.add_command('dropdb', DropDb())
    manager.add_command('runserver', CustomServer())
    manager.add_command('shell', CustomShell())
    manager.run()
