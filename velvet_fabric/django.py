import sys
import imp
from fabric.api import *
from fabric.colors import green

from .server import virtualenv
from .db import create_postgres_db, create_mysql_db
from . import PROJECT_NAME, PROJECT_PATH


@task
def init():
    create_schemas()
    syncdb()

    if env.environment is 'development':
        set_fake_pw()

    print(green('initialize'))


def get_schemas():
    with virtualenv():
        # print env.settings_module

        # # since it's dynamic, it's a fiasco the fabric propousal
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_NAME+'.'+env.settings_module)
        # django.settings_module(PROJECT_NAME+'.'+env.settings_module)
        # from django.conf import settings

        sys.path.append(PROJECT_PATH+'/'+PROJECT_NAME)
        fp, pathname, description = imp.find_module(env.settings_module)
        settings = imp.load_module(env.settings_module, fp, pathname, description)

        return settings.DATABASES


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
    schema = get_schemas()[name]

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
