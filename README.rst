===============================
Velvet Fabric
===============================

.. image:: https://badge.fury.io/py/velvet_fabric.png
    :target: http://badge.fury.io/py/velvet_fabric

.. image:: https://travis-ci.org/iknite/velvet_fabric.png?branch=master
        :target: https://travis-ci.org/iknite/velvet_fabric

.. image:: https://pypip.in/d/velvet_fabric/badge.png
        :target: https://crate.io/packages/velvet_fabric?version=latest


Automatize sysadmin tasks, elegantly adaptable and scalable.
Supports for dependency installing, environment provisioning and typical server
tasks.

* Free software: BSD license
* Documentation: http://velvet_fabric.rtfd.org.


Why in the hell this project has sense?
---------------------------------------

Because all the other good tools I've tried like Puppet, Chef, SaltStack or
juju, ends in a tons of files and configurations, server requirements, special
MAAS machines, you name it.

If you're use a Barebone server, to deploy projects, using all those are
oveshooters for this scenario.

Typical velvet fabric uses ends with a single conf file `fabfile.py` and
`/deploy` folder in your project. No magic. Easy enough, right?


No magic? I want unicorns!!
---------------------------

Better unicorn at all, ZERO server requirements.

It relies in what you can find in a minimum fresh installation
(for example Ubuntu 12.04), only with openssh-server. The Cleanest the server
the better. DRY/KISS principle here. The logic happens in your machine spitting
bash script, all thanks to the good ol' `fabric`.

You already know python, right? You know everything you need to use it.

Installation.
-------------

.. code-block:: bash
    :linenos:
    pip install velvet_fabric

Usage
-----

Create a `fabfile.py` and add something like:

.. code-block:: python
    :linenos:

    from os.path import dirname, realpath

    PROJECT_PATH = dirname(realpath(__file__))
    PROJECT_NAME = 'example'

    DEVELOPMENT_DEPENDENCIES = {
        'base': [
            'git',
        ],
        'Linux': [
            'nginx',
            'uwsgi',
            'memcached',
            'python-dev',
            'python-pip',
            'postgresql-9.1',
            'postgresql-server-dev-9.1',
            'postgresql-9.1-postgis',
        ],
        'Darwin': [
            'postgresql',
        ]
    }

    PRODUCTION_DEPENDENCIES = {
        'Linux': DEVELOPMENT_DEPENDENCIES['base'] +
        DEVELOPMENT_DEPENDENCIES['Linux'] + [
            'postfix',
        ],
    }

    STAGING_DEPENDENCIES = PRODUCTION_DEPENDENCIES

    ENVIRONMENT = {
        'STAGING': {
            'user': 'dev'
        },
        'PRODUCTION': {
            'hosts':  ('my-example.com',),
        }
    }

    from velvet_fabric.api import *

    # now begin your deploy tasks or fetch some examples in the demos section.



.. image:: https://d2weczhvl823v0.cloudfront.net/velvet-fabric/velvet-fabric/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

