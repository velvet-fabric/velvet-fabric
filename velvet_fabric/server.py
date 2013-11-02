import datetime
from contextlib import contextmanager
from fabric.api import *
from .settings import ENVIRONMENT, WRAPPER_PATH
from . import SED_RUN, PIP_RUN, BASHRC_HOME, WORKON_HOME, check


@task
def use(env_name='DEVELOPMENT'):
    for i in ENVIRONMENT[env_name]:
        env[i] = ENVIRONMENT[env_name][i]


@contextmanager
def virtualenv(env_name='DEVELOPMENT'):
    if 'directory' not in env:
        use(env_name)
    with cd(env.directory):
        with prefix(env.activate):
                yield


@task
def authenticate():
    #don't forget it's local because it should be running in each machine.
    local('cat ~/.ssh/id_rsa.pub | ssh {}@{} "mkdir -p ~/.ssh; ' +
          'cat >> ~/.ssh/authorized_keys"'.format(env.user, env.host))


@task
def create_folder(dir=None):
    sudo('mkdir -p {}'.format(dir))


@task
def create_user(user=None):
    user = check(user, 'user: Unix user.')
    sudo('passwd {user}'.format(user=user))


@task
def make_virtualenv():
    bashrc({'WORKON_HOME': WORKON_HOME})
    chown(args='-R', user='www-data', path=WORKON_HOME)
    sudo('pip install virtualenvwrapper')
    run('source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv {}'
        .format(PROJECT_NAME))


@task
def chown(user=None, group=None, path=None, args=''):
    group = user if not group else group
    sudo('chown {args} {user}:{group} {path}'.
         format(user=user, group=group, path=path, args=args))


@task
def install_requirements(args=''):
    """
    Install requirements
    """
    with virtualenv():
        run(PIP_RUN.format(args=args, requirements=env.requirements))


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
            warn('{} is not defined in the {} dependencies'
                 .format(env.os, env.environment))
            env.os = 'base'
    return env.os


@task
def install_dependencies(template='apt-get -y {args} install {deps}', args=''):
    """
    Install environment dependencies
    """
    with cd(env.directory):
        deps = set(env.dependencies['base']) | set(env.dependencies[get_os()])
        deps.discard(*env.dependencies['exclude'])
        sudo('apt-get update')
        sudo('apt-get upgrade')
        sudo(template.format(args=args, deps=' '.join(deps)))


@task
def upgrade_dependencies():
    """
    Upgrade environment dependencies
    """
    install_dependencies(args='--upgrade')


@task
def cp(source=None, link=None, user=None, group=None):
    with virtualenv():
        sudo('cp {dir}/{source} {link}'.
             format(dir=env.directory, source=source, link=link))
        if user:
            execute(chown, source=source, path=link, user=user, group=group)


@task
def rm(link=None):
    with virtualenv():
        sudo('rm {link}'.format(link=link))


@task
def sed(file_path=None, sed_dict=None, template=SED_RUN):
    """
    Inline replacement for files.
    """
    file_path = check(file_path, 'file_path: Absolute path to path.')
    sed_dict = check(sed_dict, 'sed_dict: Oject that replaces key with value.')

    for query, replace in sed_dict.items():
        sudo(template.format(query="{{\s*"+query+"\s*}}", replace=replace,
             file_path=file_path))


@task
def bashrc(vars=None):
    vars = check(vars,
                 'vars: dict of key, value pairs to store in {} (in uppercase)'
                 .format(BASHRC_HOME))
    run('echo "" >> {}'.format(BASHRC_HOME))
    run('echo "#velvet_fabric:{}" >> {}'.format(datetime.utcnow(), BASHRC_HOME))
    for k, v in vars.items():
        pair = '{}={}'.format(k.upper(), v)
        run('export {pair} && echo "{pair}" >> {home}'.format(
            pair=pair,
            home=BASHRC_HOME))


@task
def tail(link=None):
    with virtualenv():
        sudo('tail {link}'.format(link=link))


@task
def service(name=None, action=None):
    sudo('service {name} {action}'.format(name=name, action=action))
