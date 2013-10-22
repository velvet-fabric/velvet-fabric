from contextlib import contextmanager
from fabric.api import *
from fabric.utils import warn
from . import ENVIRONMENT, PROJECT_NAME


@task
def use(environment='DEVELOPMENT'):
    for i in ENVIRONMENT[environment]:
        env[i] = ENVIRONMENT[environment][i]


@contextmanager
def virtualenv(environment='DEVELOPMENT'):
    if not env:
        use(environment)
    with cd(env.directory):
        with prefix(env.activate):
            yield


@task
def authenticate():
    local('cat ~/.ssh/id_rsa.pub | ssh {}@{} "mkdir ~/.ssh; cat >> ~/.ssh/authorized_keys"'.format(env.user, env.host))


@task
def create_folder():
    sudo('mkdir -p {}'.format(env.directory))


@task
def make_virtualenv():
    run('pip install virtualenvwrapper')
    run('source /usr/local/bin/virtualenvwrapper.sh')
    run('mkvirtualev {}'.format(PROJECT_NAME))


@task
def install_requirements(args=''):
    """
    Install requirements
    """
    with virtualenv():
        run('pip install {} -r {}'.format(args, env.requirements))

    print(green('install_req'))


@task
def upgrade_requirements():
    """
    Upgrade requirements
    """
    install('--upgrade')


def get_os():
    if 'os' not in env or not env.os:
        env.os = run('uname -s')
        if env.os not in env.dependencies:
            warn('{} is not defined in the {} dependencies, it will install base only'.format(env.os, env.environment))
            env.os = 'base'
    return env.os


def get_deps():
    return list(
        set(env.dependencies['base']) | set(env.dependencies[get_os()]) - set(env.dependencies['exclude'])
    )


@task
def install_dependencies():
    """
    Install environment dependencies
    """
    print(' '.join(get_deps()))
    sudo(env.installer + ' '.join(get_deps()))


@task
def upgrade_dependencies():
    """
    Upgrade environment dependencies
    """
    run(env.installer + ' --upgrade ' + ' '.join(get_deps()))
