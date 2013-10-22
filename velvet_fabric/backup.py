from fabric.api import *


@task
def backup_mysql(name, user, passwd, dest_dir='/tmp/'):
    """
    Backup your MysQL database and save it to your local machine
    """
    timestamp = int(time.time())
    dest_file = '{0}{1}-{2}.sql'.format(dest_dir, name, timestamp)
    cmd = 'mysqldump {0} -u {1} -p{2} > {3}'.format(name,
                                                    user,
                                                    passwd,
                                                    dest_file)
    run(cmd)
    get(dest_file)
