from fabric.api import *
from fabric.utils import error
from fabric.colors import green
from . import PROJECT_NAME, GIT_ROOT
from .server import virtualenv


@task
def clone(url=GIT_ROOT, name=PROJECT_NAME):
    with virtualenv():
        sudo('cd .. && git clone {} {}'.format(url, name))


@task
def revert(revision):
    """
    Reverts application to selected revision, updates submodules and restarts servers.
    Usage: fab prod revert:ae7b9acb96c3fea00ab855952071570279b5d978
    """
    with virtualenv():
        run('git checkout {}'.format(revision))
        run('git submodule update')
        sudo('initctl reload uwsgi_cms', shell=False)


@task
def pull(branch='master'):
    if env.environment == 'production' and branch is not 'master':
        branch = 'master'
        error('Ignoring non master branch in production')

    with virtualenv():
        run('git checkout {}'.format(branch))
        run('git pull')
        run('git submodule init')
        run('git submodule update')

    print(green('git_update'))


@task
def do(string='--help'):
    """
    executes git commmands in envs
    """
    with cd(env.directory):
        run('git {}'.format(string))


@task
def last_version():
    """
    Shows last version. Usage: fab prod show_last_version
    """
    with cd(env.directory):
        run('git describe --exact-match')
