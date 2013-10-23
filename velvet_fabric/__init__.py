import os
import fabfile
from os.path import join

PROJECT_DIR = getattr(fabfile, 'PROJECT_DIR')
PROJECT_NAME = getattr(fabfile, 'PROJECT_NAME')

GIT_ROOT = getattr(fabfile, 'GIT_ROOT')

WSGI_FILEPATH = getattr(fabfile,
                        'WSGI_FILEPATH',
                        '{}deploy/wsgi/{}.ini'.format(PROJECT_DIR, PROJECT_NAME))


NGINX_FILEPATH = getattr(fabfile,
                         'NGINX_FILEPATH',
                         '{}deploy/nginx/{}'.format(PROJECT_DIR, PROJECT_NAME))

dependency_template = {
    'base': [],
    'exclude': []
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
        'directory': PROJECT_DIR,
        'environment': 'development',
        'requirements': 'requirements/development.txt',
        'settings_module': '{}.settings'.format(PROJECT_NAME),
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': DEVELOPMENT_DEPENDENCIES,
        'installer': 'brew install'
    },
    'STAGING': {
        'user': 'www-data',
        'hosts': ('{}.staging'.format(PROJECT_NAME),),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'staging',
        'requirements': 'requirements/staging.txt',
        'settings_module': '{}.settings_staging'.format(PROJECT_NAME),
        'activate': '/bin/bash {}'.format(join('~/.virtualenvs', PROJECT_NAME, 'bin/activate')),
        'dependencies': STAGING_DEPENDENCIES,
        'installer': 'apt-get -y --threads=5 {args} install {deps}'
    },
    'PRODUCTION': {
        'user': 'root',
        'hosts': ('{}.com'.format(PROJECT_NAME)),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'production',
        'requirements': 'requirements/production.txt',
        'settings_module': '{}.settings_production'.format(PROJECT_NAME),
        'activate': '/bin/bash {}'.format(join('~/.virtualenvs', PROJECT_NAME, 'bin/activate')),
        'dependencies': PRODUCTION_DEPENDENCIES,
        'installer': 'apt-get -y --threads=5 {args} install {deps}'
    }
}


def update_environment(new_env):
    for k, v in new_env.items():
        if k in ENVIRONMENT:
            ENVIRONMENT[k].update(v)

update_environment(getattr(fabfile, 'ENVIRONMENT', ENVIRONMENT))
