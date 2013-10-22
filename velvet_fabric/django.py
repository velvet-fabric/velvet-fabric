import os

from fabric.api import *
from fabric.colors import green
from .env import virtualenv
from .db import create_postgres_db, create_mysql_db


@task
def init():
    """
    Start the application to run.
    """

    #set_dependencies()
    if env.environment is not 'development':
        git_update()
    create_schemas()
    syncdb()

    if env.environment is 'development':
        set_fake_pw()

    print(green('initialize'))


def get_schemas():
    with virtualenv():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", env.settings_module)
        from django.conf.settings import DATABASES
        return DATABASES


@task
def create_schemas():
    """
    Use the django.settings to create the users and the dbs.
    """

    for name in get_schemas():
        create_schema(name)

    print(green('ALL SCHEMAS CREATED'))


@task
def create_schema(name):
    schema = get_schemas()['name']

    if 'sqlite' in schema['ENGINE']:
        print(green('schema for sqlite is ready'))
        return

    if 'postgres' in schema['ENGINE']:
        create_postgres_db(schema)

    elif 'mysql' in schema['ENGINE']:
        create_mysql_db(schema)


@task
def set_fake_pw(password='admin'):
    """
    Reset all use passwords to a fake value
    """
    fake = raw_input('Password (leave blank to use \'admin\'):')

    with virtualenv():
        run('python manage.py set_fake_passwords --password={0}'.format(fake if fake != '' else 'admin'))

    print(green('set_fake_pw'))


@task
def syncdb():
    """
    Executes 'syncdb' and 'migrate' commands
    """

    with virtualenv():
        run('python manage.py syncdb --noinput')
        run('python manage.py migrate')
