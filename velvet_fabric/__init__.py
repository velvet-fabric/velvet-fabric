import os
import fabfile
from os.path import join
from fabric.operations import prompt

PROJECT_PATH = getattr(fabfile, 'PROJECT_PATH')
PROJECT_NAME = getattr(fabfile, 'PROJECT_NAME')
BASHRC_HOME = getattr(fabfile, 'BASHRC_HOME', '~/.bashrc')
WORKON_HOME = getattr(fabfile, 'WORKON_HOME', '/var/www/.virtualenvs')
MYSQL_RUN = getattr(fabfile, 'MYSQL_RUN',
                    'echo "{actions}" | mysql -u root -p{db_password}')
PSQL_RUN = getattr(fabfile, 'PSQL_RUN',
                   '{psql} -d postgres -c "{step}"')
WRAPPER_PATH = getattr(fabfile, 'WRAPPER_PATH',
                       'source /usr/local/bin/virtualenvwrapper.sh')

SED_RUN = getattr(fabfile, 'SED_RUN',
                  "sed -i 's/{query}/{replace}/' {file_path}")
TAIL_RUN = getattr(fabfile, 'TAIL_RUN', 'tail -f {file_path}')
PIP_RUN = getattr(fabfile, 'PIP_RUN', 'pip install {args} -r {requirements}')

dependency_template = {'base': [], 'exclude': ['']}
DEVELOPMENT_DEPENDENCIES = dependency_template.copy()
STAGING_DEPENDENCIES = dependency_template.copy()
PRODUCTION_DEPENDENCIES = dependency_template.copy()

DEVELOPMENT_DEPENDENCIES.update(getattr(fabfile, 'DEVELOPMENT_DEPENDENCIES',
                                {}))
STAGING_DEPENDENCIES.update(getattr(fabfile, 'STAGING_DEPENDENCIES', {}))
PRODUCTION_DEPENDENCIES.update(getattr(fabfile, 'PRODUCTION_DEPENDENCIES', {}))


# SYS_REQUIREMENTS defines pip requirements for the whole system, useful for
# installing uWSGI system-wide
#
# Example:
# PRODUCTION_SYS_REQUIREMENTS = [
#     'uwsgi'
# ]
DEVELOPMENT_SYS_REQUIREMENTS = getattr(fabfile, 'DEVELOPMENT_SYS_REQUIREMENTS', [])
STAGING_SYS_REQUIREMENTS = getattr(fabfile, 'STAGING_SYS_REQUIREMENTS', [])
PRODUCTION_SYS_REQUIREMENTS = getattr(fabfile, 'PRODUCTION_SYS_REQUIREMENTS', [])

ENVIRONMENT = {
    'DEVELOPMENT': {
        'user': os.environ['USER'],
        'hosts': ('localhost',),
        'directory': PROJECT_PATH,
        'environment': 'development',
        'requirements': 'requirements/development.txt',
        'settings_module': 'settings',
        'activate': '/var/www/.virtualenvs/{}/bin/activate'.format(PROJECT_NAME),
        'dependencies': DEVELOPMENT_DEPENDENCIES,
        'sys_requirements': DEVELOPMENT_SYS_REQUIREMENTS,
        'installer': 'brew install {args} {deps}'
    },
    'STAGING': {
        'user': PROJECT_NAME,
        'hosts': ('{}.staging'.format(PROJECT_NAME),),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'staging',
        'requirements': 'requirements/staging.txt',
        'settings_module': 'settings_staging',
        'activate': '/var/www/.virtualenvs/{}/bin/activate'.format(PROJECT_NAME),
        'dependencies': STAGING_DEPENDENCIES,
        'sys_requirements': STAGING_SYS_REQUIREMENTS,
        'installer': 'apt-get -y {args} install {deps}'
    },
    'PRODUCTION': {
        'user': PROJECT_NAME,
        'hosts': ('{}.com'.format(PROJECT_NAME)),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'production',
        'requirements': 'requirements/production.txt',
        'settings_module': 'settings_production',
        'activate': '/var/www/.virtualenvs/{}/bin/activate'.format(PROJECT_NAME),
        'dependencies': PRODUCTION_DEPENDENCIES,
        'sys_requirements': PRODUCTION_SYS_REQUIREMENTS,
        'installer': 'apt-get -y {args} install {deps}'
    }
}


def update_environment(new_env):
    for k, v in new_env.items():
        if k in ENVIRONMENT:
            ENVIRONMENT[k].update(v)

update_environment(getattr(fabfile, 'ENVIRONMENT', ENVIRONMENT))


def check(value=None, text=None, key=None, default=None, validate=None):
    if not validate:
        validate = r'^.+$'
    return value if value else prompt(text, key, default, validate)
