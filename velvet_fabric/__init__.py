import os
import fabfile
from os.path import join

PROJECT_PATH = getattr(fabfile, 'PROJECT_PATH')
PROJECT_NAME = getattr(fabfile, 'PROJECT_NAME')

GIT_ROOT = getattr(fabfile, 'GIT_ROOT')

WSGI_LINK = getattr(fabfile, 'WSGI_LINK',
                    '/etc/uwsgi/apps-enabled/{}'.format(PROJECT_NAME))
WSGI_FILEPATH = getattr(fabfile, 'WSGI_FILEPATH', 'deploy/wsgi.ini')


NGINX_LINK = getattr(fabfile, 'NGINX_LINK',
                     '/etc/nginx/sites-enabled/{}'.format(PROJECT_NAME))
NGINX_FILEPATH = getattr(fabfile, 'NGINX_FILEPATH', 'deploy/nginx.conf')


POSTGRES_LINK = getattr(fabfile, 'POSTGRES_LINK',
                        '/etc/postgresql/9.1/main/pg_hba.conf')
POSTGRES_FILEPATH = getattr(fabfile, 'POSTGRES_FILEPATH', 'deploy/postgres.conf')


dependency_template = {
    'base': [],
    'exclude': ['']
}

DEVELOPMENT_DEPENDENCIES = dependency_template.copy()
STAGING_DEPENDENCIES = dependency_template.copy()
PRODUCTION_DEPENDENCIES = dependency_template.copy()

DEVELOPMENT_DEPENDENCIES.update(getattr(fabfile, 'DEVELOPMENT_DEPENDENCIES', {}))
STAGING_DEPENDENCIES.update(getattr(fabfile, 'STAGING_DEPENDENCIES', {}))
PRODUCTION_DEPENDENCIES.update(getattr(fabfile, 'PRODUCTION_DEPENDENCIES', {}))

ENVIRONMENT = {
    'DEVELOPMENT': {
        'user': os.environ['USER'],
        'hosts': ('localhost',),
        'directory': PROJECT_PATH,
        'environment': 'development',
        'requirements': 'requirements/development.txt',
        'settings_module': 'settings',
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': DEVELOPMENT_DEPENDENCIES,
        'installer': 'brew install {args} {deps}'
    },
    'STAGING': {
        'user': 'www-data',
        'hosts': ('{}.staging'.format(PROJECT_NAME),),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'staging',
        'requirements': 'requirements/staging.txt',
        'settings_module': 'settings_staging',
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': STAGING_DEPENDENCIES,
        'installer': 'apt-get -y {args} install {deps}'
    },
    'PRODUCTION': {
        'user': 'root',
        'hosts': ('{}.com'.format(PROJECT_NAME)),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'production',
        'requirements': 'requirements/production.txt',
        'settings_module': 'settings_production',
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': PRODUCTION_DEPENDENCIES,
        'installer': 'apt-get -y {args} install {deps}'
    }
}


def update_environment(new_env):
    for k, v in new_env.items():
        if k in ENVIRONMENT:
            ENVIRONMENT[k].update(v)

update_environment(getattr(fabfile, 'ENVIRONMENT', ENVIRONMENT))
