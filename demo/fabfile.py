from os.path import dirname, realpath

PROJECT_PATH = dirname(realpath(__file__))
PROJECT_NAME = 'example'
GIT_ROOT = 'https://iknite@bitbucket.org/velvet-fabric/dango-deploy.git'

WSGI_LINK = '/etc/uwsgi/apps-enabled/{}.ini'.format(PROJECT_NAME)
WSGI_FILEPATH = 'deploy/uwsgi.ini'
WSGI_LOG = '/tmp/uwsgi.{project_name}.log'

UPSTART_UWSGI_LINK = '/etc/init.d/uwsgi.conf'
UPSTART_UWSGI_FILEPATH = 'deploy/upstart_uwsgi.conf'
UPSTART_UWSGI_LOG = '/var/log/uwsgi/upstart_uwsgi.log'

NGINX_LINK = '/etc/nginx/sites-enabled/{}'.format(PROJECT_NAME)
NGINX_FILEPATH = 'deploy/nginx.conf'
NGINX_LOG = '/var/log/nginx/{project_name}.{level}.log'

POSTGRES_LINK = '/etc/postgresql/9.1/main/pg_hba.conf'
POSTGRES_FILEPATH = 'deploy/postgres.conf'
POSGRES_LOG = '/var/log/postgresql/postgresql-9.1-main.log'

DEVELOPMENT_DEPENDENCIES = {
    'base': [
        'git',
        'phantomjs',
    ],
    'Linux': [
        'openssh-server',
        'nginx',
        'uwsgi',
        'memcached',
        'python-dev',
        'python-pip',
        'python-m2crypto',
        'liblcms1-dev',
        'libtiff4-dev',
        'libwebp-dev',
        'g++',
        'curl',
        'swig',
        'libssl-dev',
        'apache2-utils',
        'postgresql-9.1',
        'postgresql-server-dev-9.1',
        'postgresql-9.1-postgis',
        'libjpeg8-dev',
        'libpng12-dev',
    ],
    'Darwin': [
        'postgresql',
        'git-extra',
        'libjpeg',
        'freetype',
    ]
}

PRODUCTION_DEPENDENCIES = {
    'Linux': DEVELOPMENT_DEPENDENCIES['base'] +
    DEVELOPMENT_DEPENDENCIES['Linux'] + [
        'postfix',
    ],
}

STAGING_DEPENDENCIES = PRODUCTION_DEPENDENCIES

ENVIRONMENT = {
    'STAGING': {
        'user': 'dev'
    },
    'PRODUCTION': {
        'user': 'root',
        'hosts':  ('example.com',),
    }
}

from velvet_fabric.api import *


@task
def dev():
    server.use()


@task
def staging():
    server.use('STAGING')


@task
def prod():
    server.use('PRODUCTION')


@task
def unbox():
    with settings(user='root'):
        server.create_user(env.user)
        server.create_folder(env.dirxectory)
    with cd(env.directory):
        server.chown(args='-R', user=env.user, path=env.directory)
        server.authenticate()
        server.install_dependencies(template=env.installer)
        run('pip install uwsgi')
        run('{}/deploy/install_node.sh v0.10.21'.format(env.directory))
        server.make_virtualenv()
        git.clone(GIT_ROOT, PROJECT_NAME)
        server.install_requirements()
        server.chown(args='-R', user='www-data', path=env.directory)
        server.rm(POSTGRES_LINK)
        server.cp(POSTGRES_FILEPATH, POSTGRES_LINK, 'postgres')
        service('postgresql', 'restart')
        server.rm(UPSTART_UWSGI_LINK)
        server.cp(UPSTART_UWSGI_FILEPATH, UPSTART_UWSGI_LINK)
        django.init()


@task
def upgrade():
    with server.virtualenv():
        run('npm install')
    server.install_dependencies()
    server.upgrade_requirements()


@task
def wire():
    git.pull()
    # server.cp(NGINX_FILEPATH, NGINX_LINK)
    # server.sed(NGINX_LINK, {
    #     'project_name': PROJECT_NAME
    # })

    server.rm(WSGI_LINK)
    server.cp(WSGI_FILEPATH, WSGI_LINK)
    server.sed(WSGI_LINK, {
        'settings_module': env.settings_module,
        'user': env.user,
        'project_name': PROJECT_NAME
    })
    # server.chown(user='www-data', path=WSGI_LINK)
    # server.chown(user='www-data', path=NGINX_LINK)
    restart()


@task
def cut():
    server.rm(NGINX_LINK)
    server.rm(WSGI_LINK)
    restart()


@task
def nginx_log(level=None):
    level = check(level, 'level: access or error.', default='error',
                  validate=r'^access|error$')
    server.tail(NGINX_LOG.format(PROJECT_NAME, level))


@task
def wsgi_log():
        server.tail(WSGI_LOG.format(project_name=PROJECT_NAME))


@task
def upstart_log():
        server.tail(UPSTART_UWSGI_LOG.format(project_name=PROJECT_NAME))


@task
def up():
    server.service('nginx', 'start')
    run('/enc/init.d/uwsgi.conf stop')


@task
def down():
    server.service('nginx', 'stop')
    server.service('uwsgi.conf', 'stop')


@task
def restart():
    server.service('nginx', 'restart')
    with server.virtualenv():
        run('uwsgi --ini {}'.format(WSGI_LINK))
