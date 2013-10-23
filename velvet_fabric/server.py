
from fabric.api import *
from . import PROJECT_NAME, NGINX_FILEPATH, WSGI_FILEPATH, env as nv, git


@task
def wsgi_link():
    with env.virtualenv():
        run('ln -s {} /etc/wsgi/{}'.format(WSGI_FILEPATH, PROJECT_NAME))


@task
def nginx_link():
    with virtualenv():
        run('ln -s {} /etc/nginx/sites-enabled/{}'.format(NGINX_FILEPATH, PROJECT_NAME))


@task
def provisioning():
    execute(nv.create_folder)
    with cd(env.directory):
        execute(nv.chown, env.user)
        execute(nv.authenticate)
        execute(nv.install_dependencies, env.installer)
        execute(nv.make_virtualenv)
        execute(git.clone)
        execute(nv.install_requirements)
        execute(nv.chown, 'www-data')
        execute(nginx_link)
        execute(wsgi_link)
        execute(django.init)


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
