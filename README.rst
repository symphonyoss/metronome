metronome
=========

.. image:: https://img.shields.io/pypi/v/metronome.svg
         :target: https://pypi.python.org/pypi/metronome/

.. image:: https://img.shields.io/pypi/pyversions/metronome.svg
         :target: https://pypi.python.org/pypi/metronome/

.. image:: https://img.shields.io/pypi/format/metronome.svg
         :target: https://pypi.python.org/pypi/metronome/

.. image:: https://img.shields.io/badge/license-Apache%202-blue.svg
         :target: https://github.com/symphonyoss/metronome/blob/master/LICENSE

.. image:: https://travis-ci.org/symphonyoss/metronome.svg?branch=master
      :target: https://travis-ci.org/symphonyoss/metronome

.. image:: https://www.versioneye.com/user/projects/584f7bad5d8a550042585f60/badge.svg?style=flat-square
      :target: https://www.versioneye.com/user/projects/584f7bad5d8a550042585f60


About
-----

metronome is Symphony bot designed to provide end to end diagnostic information to the 
Symphony Engineering Services team.  This bot is fairly simple. 

It logs into your symphony pod, and then joins a cross pod chat room and begins to send messages with
some basic information about the pod environment.  

Our ES bot listens in and adds information to our local trends database and can alert our team to any problems
directly as needed.

Installation
------------

this application can be installed as an rpm or from a python setup.py.

.. code:: bash

   python setup.py install

will install this application, however it is recommended to install it within a virtualenv

You will also need to complete a metronome config file.

Configuration
-------------

Example config file:

.. code:: text

   [symphony]
   # uri for /pod endpoint
   symphony_pod_uri: https://vanityname.symphony.com/
   symphony_keymanager_uri: https://vanityname.symphony.com:8444/
   symphony_agent_uri: https://vanityname.symphony.com:8444/
   symphony_sessionauth_uri: https://vanityname.symphony.com:8444/
   symphony_p12: /etc/es-bot/certs/bot.user100.p12
   symphony_pwd: passwordforPKCSfile
   symphony_sid: example_gLc8hdZBHut6CUJnwMmzH3___qcqBgDKdA

Execution
---------

.. code:: text

   metronome.py -h
   usage: metronome.py [-h] [-c [CONFIG]] [-l [LOG]] [-d] [--counter [COUNTER]]

   metronome bot

   optional arguments:
     -h, --help            show this help message and exit
     -c [CONFIG], --config [CONFIG]
                        specify path to config file
     -l [LOG], --log [LOG]
                        specify path to log file
     -d, --debug           debug logging
     --counter [COUNTER]   specify path to cache counter
