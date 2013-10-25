# sintactic sugar for import nicely in fabfile.
from fabric.api import *
from . import django, backup, db, server, git, tests
