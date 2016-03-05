===========
home_config
===========

*home_config* is a `Python <https://www.python.org/downloads/>`_ library
to easily create and prioritize the config files for your application.

It creates configuration files in user
`home directory <https://en.wikipedia.org/wiki/Home_directory>`_
and program directory.
Creates them if they do not exists.
Makes it easy to access and handle them.
The file in home directory will take precedence over the one in program directory.

Using *home_config*, you can distribute your packages with a default configuration file.
*home_config* will detect your home directory and creates a configuration file there.
If both home directory and program directory contains a configuration file,
the one in the home directory will have a priority.

The intention of the package is to freely distribute your Python applications with default
configuration file, and use *home_config* to programmatically create a configuration file for user.


User Guide
----------

Full Sample
+++++++++++

.. code-block:: python

    import ConfigParser
    from home_config import HomeConfig

    default_content = """
    [Numbers]
    one=1
    two=2
    three=3
    """.strip()
    config_file_name = "my_settings.cfg"

    hc = HomeConfig(config_file_name=config_file_name)
    hc.create_in_program_dir(default_content=default_content)
    hc.create_in_home_dir(default_content=default_content)
    config = ConfigParser.RawConfigParser()
    config.read(hc.get_active_config_file_path())
    # the one in home directory will be read.

    lucky_number = config.get("Numbers", "two")


Installation
------------

The easiest way to install this is to use `pip`, as follows:

.. code-block::

    pip install home_config

Don't you have `pip`?
See the `installation guide of pip <https://pip.pypa.io/en/stable/installing/>`_.


How to Run Tests
----------------

You need `nose <https://nose.readthedocs.org/en/latest/>`_ for testing.
Install *nose* like this:

.. code-block::

    pip install nose

Start the tests for *home_config*:

.. code-block::

    cd /root/directory/of/home_config
    nosetests


Contribution
------------
Feel free to send fork requests, feedback and comments here:
https://github.com/caglartoklu/home_config


License
-------

Licensed with 2-clause license ("Simplified BSD License" or "FreeBSD License").
See the LICENSE.txt file.
