from contextlib import contextmanager
from fabric.api import *
from fabric.utils import warn
from . import ENVIRONMENT, PROJECT_NAME


@task
def use(env_name='DEVELOPMENT'):
    for i in ENVIRONMENT[env_name]:
        env[i] = ENVIRONMENT[env_name][i]


@contextmanager
def virtualenv(environment='DEVELOPMENT'):
    if not env:
        use(environment)
    with cd(env.directory):
        with prefix('source /usr/local/bin/virtualenvwrapper.sh'):
            with prefix(env.activate):
                yield


@task
def authenticate():
    #don't forget it's local because it shoulb be running here.
    local('cat ~/.ssh/id_rsa.pub | ssh {}@{} "mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys"'.format(env.user, env.host))


@task
def create_folder(dir=None):
    sudo('mkdir -p {}'.format(dir))


@task
def make_virtualenv():
    sudo('pip install virtualenvwrapper')
    run('source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv {}'.format(PROJECT_NAME))


@task
def chown(user='www-data', group=None, path=None, args=''):
    group = user if not group else group
    sudo('chown {args} {user}:{group} {path}'.
         format(user=user, group=group, path=path, args=args))


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
    install_requirements('--upgrade')


def get_os():
    if 'os' not in env or not env.os:
        env.os = run('uname -s')
        if env.os not in env.dependencies:
            warn('{} is not defined in the {} dependencies, it will install base only'.format(env.os, env.environment))
            env.os = 'base'
    return env.os


@task
def install_dependencies(template='apt-get install {args} {deps}', args=''):
    """
    Install environment dependencies
    """
    with cd(env.directory):
        deps = set(env.dependencies['base']) | set(env.dependencies[get_os()])
        deps.discard(*env.dependencies['exclude'])
        sudo('apt-get update')
        sudo(template.format(args=args, deps=' '.join(deps)))


@task
def upgrade_dependencies():
    """
    Upgrade environment dependencies
    """
    install_dependencies(args='--upgrade')


def link(source=None, link=None, user=None, group=None):
    with virtualenv():
        sudo('cp {dir}/{source} {link}'.
             format(dir=env.directory, source=source, link=link))
        if user:
            execute(chown, source=source, path=link, user=user, group=group)


def unlink(link=None):
    with virtualenv():
        sudo('rm {link}'.format(link=link))


@task
def service(name=None, action=None):
    sudo('service {name} {action}'.format(name=name, action=action))
