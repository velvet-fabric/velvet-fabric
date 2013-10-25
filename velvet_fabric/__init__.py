import os
import fabfile
from os.path import join
from fabric.operations import prompt

PROJECT_PATH = getattr(fabfile, 'PROJECT_PATH')
PROJECT_NAME = getattr(fabfile, 'PROJECT_NAME')
MYSQL_RUN = getattr(fabfile, 'MYSQL_RUN',
                    'echo "{actions}" | mysql -u root -p{db_password}')
PSQL_RUN = getattr(fabfile, 'PSQL_RUN',
                   '{psql} -d postgres -c "{step}"')
WRAPPER_PATH = getattr(fabfile, 'WRAPPER_PATH',
                       'source /usr/local/bin/virtualenvwrapper.sh')

SED_RUN = getattr(fabfile, 'SED_RUN', "sed -i 's/{query}/{replace}/' {file_path}")
TAIL_RUN = getattr(fabfile, 'TAIL_RUN', 'tail -f {file_path}')
PIP_RUN = getattr(fabfile, 'PIP_RUN', 'pip install {args} -r {requirements}')

dependency_template = {'base': [], 'exclude': ['']}
DEVELOPMENT_DEPENDENCIES = dependency_template.copy()
STAGING_DEPENDENCIES = dependency_template.copy()
PRODUCTION_DEPENDENCIES = dependency_template.copy()

DEVELOPMENT_DEPENDENCIES.update(getattr(fabfile, 'DEVELOPMENT_DEPENDENCIES', {}))
STAGING_DEPENDENCIES.update(getattr(fabfile, 'STAGING_DEPENDENCIES', {}))
PRODUCTION_DEPENDENCIES.update(getattr(fabfile, 'PRODUCTION_DEPENDENCIES', {}))

ENVIRONMENT = {
    'DEVELOPMENT': {
        'user': os.environ['USER'],
        'hosts': ('localhost',),
        'directory': PROJECT_PATH,
        'environment': 'development',
        'requirements': 'requirements/development.txt',
        'settings_module': 'settings',
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': DEVELOPMENT_DEPENDENCIES,
        'installer': 'brew install {args} {deps}'
    },
    'STAGING': {
        'user': PROJECT_NAME,
        'hosts': ('{}.staging'.format(PROJECT_NAME),),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'staging',
        'requirements': 'requirements/staging.txt',
        'settings_module': 'settings_staging',
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': STAGING_DEPENDENCIES,
        'installer': 'apt-get -y {args} install {deps}'
    },
    'PRODUCTION': {
        'user': PROJECT_NAME,
        'hosts': ('{}.com'.format(PROJECT_NAME)),
        'directory': join('/var/www/', PROJECT_NAME),
        'environment': 'production',
        'requirements': 'requirements/production.txt',
        'settings_module': 'settings_production',
        'activate': 'workon {}'.format(PROJECT_NAME),
        'dependencies': PRODUCTION_DEPENDENCIES,
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
