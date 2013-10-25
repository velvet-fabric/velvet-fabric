from fabric.api import *


@task
def backup_mysql(name=None, user=None, passwd=None, dest_dir='/tmp/'):
    """
    Backup your MysQL database and save it to your local machine
    """
    name = check(name, 'name: The database to backup.')
    user = check(user, 'user: The database user.')
    dest_dir = check(dest_dir, 'dest_dir: The server folder to store.')

    timestamp = int(time.time())
    dest_file = '{0}{1}-{2}.sql'.format(dest_dir, name, timestamp)
    cmd = 'mysqldump {0} -u {1} -p{2} > {3}'.format(name, user, passwd,
                                                    dest_file)
    run(cmd)
    get(dest_file)
    return dest_file
