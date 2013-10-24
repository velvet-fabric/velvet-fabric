from fabric.api import *
from fabric.colors import green, red
from fabric.utils import error


def is_schema_misconfigured(schema={}):
    for i in ['ENGINE', 'NAME', 'USER', 'PASSWORD', 'HOST', 'PORT']:
        if not i in schema or schema[i] is None:
            error('schema[{}] misconfigured'.format(i))
            return True

    return False


def create_mysql_db(schema, db_password=None):
    if is_schema_misconfigured(schema):
        return

    schema['HOST'] == 'localhost' if schema['HOST'] == '' else schema['HOST']
    schema['PORT'] == ':'+schema['PORT'] if schema['PORT'] is not '' else ''
    if db_password is None:
        db_password = raw_input('Enter mysql root password:')

    actions = [
        "CREATE DATABASE IF NOT EXISTS {NAME}",
        "GRANT ALL PRIVILEGES ON {NAME}.* TO '{USER}'@'{HOST}{PORT}' IDENTIFIED BY '{PASSWORD}'",
    ]
    bash = "echo \"{}\" | mysql -u root -p{mysql_password}".format("; ".join(actions), mysql_password=db_password)

    run(bash.format(**schema))

    print(green('schema for mysql is ready'))


def create_postgres_db(schema):
    """
    Create a PostgreSQL db and user
    """
    if is_schema_misconfigured(schema):
        return

    db_command = 'sudo -u postgres psql' if 'Darwin' is not run('uname -s') \
                 else 'psql'

    actions = (
        "drop database if exists {NAME}",
        "drop role if exists {USER}",
        "create user {USER} with password '{PASSWORD}'",
        "create database {NAME} with owner {USER} encoding='utf8' template template0",
    )
    for step in actions:
        run('{} -d postgres -c "{}"'.format(db_command, step).format(**schema))

    print(green('Schema for Postgres is ready'))


@task
def activate_postgis():
    """
    Create a PostGIS extension for postgres
    """

    with credentials():
        actions = (
            'CREATE EXTENSION postgis',  # Enable PostGIS (includes raster)
            'CREATE EXTENSION postgis_topology',  # Enable Topology
            'CREATE EXTENSION fuzzystrmatch',  # fuzzy matching needed for Tiger
            'CREATE EXTENSION postgis_tiger_geocoder',  # Enable US Tiger Geocoder
        )
        for step in actions:
            run('psql -d postgres -c "{}"'.format(step))

    print(green('PostGIS is ready'))


@task
def drop_postgres_db(user=None, db=None):
    """
    Drop PostgreSQL db
    """
    if user is None or db is None:
        print(red('Please, provide dbname and user'))
        return
    run('dropdb {0}'.format(db, user))


@task
def rebuild_postgres_db(user=None, db=None, sync=0):
    """
    Drop and create a PostgreSQL db
    """
    if user is None or db is None:
        print(red('Please, provide dbname and user'))
        return
    drop_postgres_db(user, db)
    create_postgres_db(user, db)
    if sync == '1':
        syncdb()
