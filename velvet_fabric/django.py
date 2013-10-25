import sys
import imp
from fabric.api import *
from fabric.colors import green
from fabric.utils import error

from .overrides import run
from .server import virtualenv
from .db import mysql_create, postgres_create
from . import PROJECT_PATH, PROJECT_NAME, check


def get_schemas():
    with virtualenv():
        # print env.settings_module

        # # since it's dynamic, it's a fiasco the fabric propousal
        # os.environ.setdefault("DJANGO_SETTINGS_MODULE", PROJECT_NAME+'.' +
        #                       env.settings_module)
        # django.settings_module(PROJECT_NAME+'.'+env.settings_module)
        # from django.conf import settings

        sys.path.append(PROJECT_PATH+'/'+PROJECT_NAME)
        fp, pathname, description = imp.find_module(env.settings_module)
        settings = imp.load_module(env.settings_module, fp, pathname,
                                   description)

        return settings.DATABASES


@task
def create_schemas():
    """
    Use the django.settings to create the users and the dbs.
    """

    for name in get_schemas():
        create_schema(name)

    print(green('ALL SCHEMAS CREATED'))


def is_schema_misconfigured(schema={}):
    for i in ['ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']:
        if not i in schema or schema[i] is None:
            error('schema[{}] misconfigured'.format(i))
            return True

    return False


@task
def create_schema(name=None):
    name = check(name, 'name: Which schema form settings.DATABASES?',
                 default='default')
    schema = get_schemas()[name]

    if 'sqlite' in schema['ENGINE']:
        return

    if 'postgres' in schema['ENGINE']:
        postgres_create(name=schema['NAME'], user=schema['USER'],
                        password=schema['PASSWORD'])

    elif 'mysql' in schema['ENGINE']:
        mysql_create(name=schema['NAME'], user=schema['USER'],
                     password=schema['PASSWORD'], host=schema['HOST'],
                     port=schema['PORT'])


@task
def set_fake_pw(password='admin'):
    """
    Reset all use passwords to a fake value
    """
    fake = raw_input('Password (leave blank to use \'admin\'):')

    with virtualenv():
        run('python manage.py set_fake_passwords --password={0}'
            .format(fake if fake != '' else 'admin'))

    print(green('set_fake_pw'))


@task
def syncdb():
    """
    Executes 'syncdb' and 'migrate' commands
    """
    with virtualenv():
        run('python manage.py syncdb --noinput')
        run('python manage.py migrate')
