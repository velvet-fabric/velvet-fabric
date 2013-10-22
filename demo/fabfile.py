from os.path import dirname, realpath
from fabric.api import *

PROJECT_DIR = dirname(realpath(__file__))
PROJECT_NAME = 'rayofuego'

DEVELOPMENT_DEPENDENCIES = {
    'base': [
        'git',
        'git-extra',
        'phantomjs',
    ],
    'Linux': [
        'libjpeg8-dev',
        'libpng12-dev',
    ],
    'Darwin': [
        'postgresql',
        'libjpeg',
        'freetype',
    ]
}

PRODUCTION_DEPENDENCIES = {
    'base': DEVELOPMENT_DEPENDENCIES['base'] + [
        'memcached',
        'solr',
    ],
    'Linux': DEVELOPMENT_DEPENDENCIES['Linux'] + [
        'open-ssh',
        'postfix',
        'python-pip'
        'liblcms1-dev',
        'libtiff4-dev',
        'libwebp-dev',
        'g++',
        'curl',
        'libssl-dev',
        'apache2-utils',
        'postgresql-9.1',
        'postgresql-9.1-postgis',
    ],
    'Darwin': DEVELOPMENT_DEPENDENCIES['Darwin'] + [
        'libtiff',
        'littleCMS',
        'node',
        'postgres',
        'postgis',
    ],
    'exclude': [
        'phantomjs'
    ]
}

STAGING_DEPENDENCIES = PRODUCTION_DEPENDENCIES

ENVIRONMENT = {
    'STAGING': {
        'user': 'dev'
    }
}

from velvet_fabric import backup, db, django, env, git, server, tests
[backup, db, django, env, git, server, tests]  # annoying alerts...


@task
def dev():
    env.use()


@task
def staging():
    env.use('STAGING')


@task
def production():
    env.use('PRODUCTION')
