from fabric.api import *
from . import POSTGRES_FILEPATH, POSTGRES_LINK, WSGI_FILEPATH, \
    WSGI_LINK, NGINX_FILEPATH, NGINX_LINK, server, git


@task
def unbox():
    execute(server.create_folder, env.directory)
    with cd(env.directory):
        execute(server.chown, args='-R', user=env.user, path=env.directory)
        execute(server.authenticate)
        execute(server.install_dependencies, template=env.installer)
        execute(server.make_virtualenv)
        execute(git.clone)
        execute(server.install_requirements)
        execute(server.chown, args='-R', user='www-data', path=env.directory)
        execute(unlink, POSTGRES_LINK)
        execute(link, POSTGRES_FILEPATH, POSTGRES_LINK, 'postgres')
        execute(service, 'postgresql', 'restart')
        execute(django.init)


@task
def upgrade():
    execute(server.server.upgrade_dependencies, template=env.installer)
    execute(server.server.upgrade_requirements, template=env.installer)


@task
def wire():
    execute(server.link, NGINX_FILEPATH, NGINX_LINK)
    execute(server.link, WSGI_FILEPATH, WSGI_LINK)
    execute(server.service, 'nginx', 'restart')
    execute(server.service, 'uwsgi', 'restart')


@task
def cut():
    execute(server.unlink, NGINX_LINK)
    execute(server.unlink, WSGI_LINK)


@task
def up():
    execute(server.service, 'nginx', 'start')
    execute(server.service, 'uwsgi', 'start')


@task
def stop():
    execute(server.service, 'nginx', 'stop')
    execute(server.service, 'uwsgi', 'stop')


@task
def restart():
    run("print 'hola'")
