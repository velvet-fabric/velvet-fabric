import fabfile
from fabric.api import *
from . import PROJECT_DIR, PROJECT_NAME, env as nv

WSGI_FILEPATH = getattr(fabfile,
                        'WSGI_FILEPATH',
                        '{}deploy/wsgi/{}.ini'.format(PROJECT_DIR, PROJECT_NAME))


NGINX_FILEPATH = getattr(fabfile,
                         'NGINX_FILEPATH',
                         '{}deploy/nginx/{}'.format(PROJECT_DIR, PROJECT_NAME))


@task
def wsgi_link():
    with env.virtualenv():
        run('ln -s {} /etc/wsgi/{}'.format(NGINX_FILEPATH, PROJECT_NAME))


@task
def nginx_link():
    with virtualenv():
        run('ln -s {} /etc/nginx/sites-enabled/{}'.format(NGINX_FILEPATH, PROJECT_NAME))


@task
def provisioning():
    execute(nv.create_folder)
    with cd(env.directory):
        execute(nv.authenticate)
        execute(nv.install_dependencies)
        execute(nv.make_virtualenv)
        execute(nv.install_requirements)
        execute(nginx_link)
        execute(wsgi_link)


@task
def upgrade():
    with env.virtualenv():
        execute(nv.upgrade_dependencies)
        execute(nv.upgrade_requirements)


@task
def start():
    run("print 'hola'")


@task
def stop():
    run("print 'hola'")


@task
def restart():
    run("print 'hola'")
