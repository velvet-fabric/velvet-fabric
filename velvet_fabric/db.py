from fabric.api import *
from . import MYSQL_RUN, PSQL_RUN, check


@task
def mysql_run(actions=None, format_dict=None, db_password=None, command=MYSQL_RUN):
    """
    Run MySQL commands
    """
    actions = check(actions, 'actions: A iterable of commands to perform.')
    format_dict = check(format_dict, 'format_dict: the dict for the format translations.')
    db_password = check(db_password, 'db_password: The mysql password.')

    bash = command.format(actions='; '.join(actions), db_password=db_password)
    if format_dict:
        bash = bash.format(**format_dict)
    run(bash)


@task
def mysql_create(name=None, user=None, password=None, host=None,
                    db_password=None, port=''):
    """
    Create a MySQL db and user.
    """
    name = check(name, 'name: the database name to create.')
    user = check(user, 'user: the user to grant privileges')
    password = check(password, 'password: user\'s password')
    host = check(host, 'host: machine ', default='localhost')
    db_password = check(db_password, 'db_password: mysql password.')
    port == ':'+port if port is not '' else ''

    mysql_run((
        "CREATE DATABASE IF NOT EXISTS {name}",
        "GRANT ALL PRIVILEGES ON {name}.* TO '{user}'@'{host}{port}' IDENTIFIED BY '{password}'",
    ), {'name': name, 'user': user, 'password': password, 'host': host,
        'port': port},  db_password=db_password)


@task
def mysql_drop(name=None, user=None, db_password=None):
    """
    Create a MySQL db and user.
    """
    name = check(name, 'name: the database name to delete.')
    user = check(user, 'user: the user to remove.')
    password = check(password, 'password: user\'s password')
    host = check(host, 'host: machine ', default='localhost')
    db_password = check(db_password, 'db_password: mysql password.')
    port == ':'+port if port is not '' else ''

    mysql_run((
        "DROP DATABASE IF EXISTS {name}",
        "DROP USER {user}",
    ), {'name': name, 'user': user, 'password': password, 'host': host,
        'port': port},  db_password=db_password)


@task
def mysql_rebuild(name=None, user=None, password=None, host=None,
                     db_password=None, port=''):
    """
    Drop and create MySQL db and user.
    """
    name = check(name, 'name: the database name to create.')
    user = check(user, 'user: the user to grant privileges')
    password = check(password, 'password: user\'s password')
    host = check(host, 'host: machine ', 'mysql_host', default='localhost')
    db_password = check(db_password, 'db_password: mysql password.')
    port == ':'+port if port is not '' else ''

    drop_postgres_db(name=name, user=user, db_password=db_password)
    create_postgres_db(name=name, user=user, password=password, host=host,
                       db_password=db_password, port=port)


@task
def postgres_run(actions=None, format_dict=None, command=PSQL_RUN):
    """
    Run PostgreSQL commands.
    """
    actions = check(actions, 'actions:')
    format_dict = check(format_dict, 'format_dict:')

    psql = 'sudo -u postgres psql' if 'Darwin' is not run('uname -s') else 'psql'
    for step in actions:
        bash = command.format(psql=psql, step=step)
        if format_dict:
            bash = bash.format(**format_dict)
        run(bash)


@task
def postgres_create(name=None, user=None, password=None):
    """
    Create a PostgreSQL db and user.
    """
    name = check(name, 'name: The dabatase name to create.')
    user = check(user, 'user: the user to grant privileges.')
    password = check(password, 'password: the user\'s password')

    postgres_run((
        "create user {user} with password '{password}'",
        "create database {name} with owner {user} template template0",
    ), {'name': name, 'user': user, 'password': password})


@task
def postgres_drop(name=None, user=None):
    """
    Drop PostgreSQL db and user.
    """
    name = check(name, 'name: The dabatase name to create.')
    user = check(user, 'user: the user to grant privileges.')

    i_postgres_run((
        "drop database if exists {name}",
        "drop role if exists {user}"
    ), {'name': name, 'user': user})


@task
def postgres_rebuild(name=None, user=None):
    """
    Drop and create a PostgreSQL db and user.
    """
    name = check(name, 'name: The dabatase name to create.')
    user = check(user, 'user: the user to grant privileges.')

    drop_postgres_db(name=name, user=user)
    create_postgres_db(name=name, user=user, password=password)


@task
def postgres_activate_postgis():
    """
    Create a PostGIS extension for postgres.
    """
    postgres_run((
        'CREATE EXTENSION postgis',  # Enable PostGIS (includes raster)
        'CREATE EXTENSION postgis_topology',  # Enable Topology
        'CREATE EXTENSION fuzzystrmatch',  # fuzzy matching needed for Tiger
        'CREATE EXTENSION postgis_tiger_geocoder',  # Enable US Tiger Geocoder
    ))
