from fabric.api import *
from fabric.contrib.console import confirm
from . import check


@task
def run(app=''):
    with settings(warn_only=True):
        result = local('./manage.py test {}'.format(app), capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")
