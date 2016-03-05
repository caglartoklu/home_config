#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Unit tests for home_config.

https://python-packaging.readthedocs.org/en/latest/testing.html
pip install nose
"""

# pylint: disable=C0103
# Disables:
# Invalid module name "atom-linter_xxxxxx"at
# line 1 col 1 in dropshadow_bed\__init__.py
# This warning occurs in in linter-pylint extension of Atom.


from __future__ import print_function
from __future__ import unicode_literals
from unittest import TestCase
import ConfigParser
import os
import os.path
import errno
import shutil
import tempfile
from home_config import HomeConfig


def _get_module_dir():
    """Return the path to the module."""
    return os.path.abspath(os.path.dirname(__file__))


def _ensure_dir_exists(dir_name):
    """Create the directory if it does not exist."""
    try:
        os.makedirs(dir_name)
    except OSError as exc:
        if exc.errno != errno.EEXIST:
            raise


class HomeConfigTestCase(TestCase):
    """Test for home_config module."""

    def setUp(self):
        """Method called to prepare the test fixture."""
        # Define temp directorys for home and program.
        # Do not pollute the file system outside the project directory.

        config_file_name = "hc_test.cfg"

        self.program_dir = tempfile.mkdtemp(prefix="tmp_hc_program_")
        # c:\\users\\muyser\\appdata\\local\\temp\\tmp_hc_program_e7wsai

        self.home_dir = tempfile.mkdtemp(prefix="tmp_hc_home_")
        # c:\\users\\muyser\\appdata\\local\\temp\\tmp_hc_home_mvacos

        _ensure_dir_exists(self.home_dir)
        _ensure_dir_exists(self.program_dir)

        self.hc = HomeConfig(config_file_name=config_file_name,
                             program_dir=self.program_dir,
                             home_dir=self.home_dir)

    def tearDown(self):
        """Method called immediately after the test method has been called."""
        # Remove the temp directorys.
        # Be cautious, remove only the directory created by the tests.
        if self.program_dir.startswith("tmp_hc_program_"):
            shutil.rmtree(self.program_dir)
        if self.home_dir.startswith("tmp_hc_home_"):
            shutil.rmtree(self.home_dir)

    def test_two_plus_two(self):
        """Proof of concept test."""
        self.assertEqual(4, 2+2)

    def test_get_config_file_name(self):
        """Test if the config file name could be retrieved as expected."""
        self.assertEqual("hc_test.cfg", self.hc.get_config_file_name())

    def test_dirs_exists(self):
        """Check if test program and data directory exists."""
        self.assertTrue(os.path.isdir(self.program_dir))
        self.assertTrue(os.path.isdir(self.home_dir))

        # check if hc could return the correct paths
        self.assertEqual(self.program_dir, self.hc.get_program_dir())
        self.assertEqual(self.home_dir, self.hc.get_home_dir())

    def test_create_and_read_config_files(self):
        """
        Create both home and program config files and check their content.

        This test creates the config file in program directory first.
        It creates the config file in home directory later.
        Checks if the content of the config file in the home directory is active.
        """
        content_in_program = """
[Numbers]
one=1
two=deux
three=3
        """.strip()

        content_in_home = """
[Numbers]
one=1
two=2
three=3
        """.strip()

        # first part of the tests are on program directory.

        config_in_program = self.hc.get_config_path_in_program_dir()
        # the file is expected to be missing at this point:
        self.assertFalse(os.path.isfile(config_in_program))
        # create the file in program directory:
        self.hc.create_in_program_dir(default_content=content_in_program)
        self.assertTrue(os.path.isfile(config_in_program))
        # the active config file should be the one in program directory
        self.assertEqual(self.hc.get_config_path_in_program_dir(),
                         self.hc.get_active_config_file_path())

        # get a value from the active config file.
        self.hc.get_active_config_file_path()
        config = ConfigParser.RawConfigParser()
        config.read(self.hc.get_active_config_file_path())
        self.assertEqual("deux", config.get("Numbers", "two"))

        # now, switch to home directory.

        config_in_home = self.hc.get_config_path_in_home_dir()
        # the file is expected to be missing at this point:
        self.assertFalse(os.path.isfile(config_in_home))
        # create the file in home directory:
        self.hc.create_in_home_dir(default_content=content_in_home)
        self.assertTrue(os.path.isfile(config_in_home))
        # the active config file should be the one in program directory
        self.assertEqual(self.hc.get_config_path_in_home_dir(),
                         self.hc.get_active_config_file_path())

        # get a value from the active config file.
        self.hc.get_active_config_file_path()
        config = ConfigParser.RawConfigParser()
        config.read(self.hc.get_active_config_file_path())
        self.assertEqual("2", config.get("Numbers", "two"))

    def test_create_and_read_config_files2(self):
        """
        Create both home and program config files and check their content.

        This test creates the config file in home directory first.
        It creates the config file in program directory later.
        Checks if the content of the config file in the home directory is active.
        """
        content_in_program = """
[Numbers]
one=1
two=deux
three=3
        """.strip()

        content_in_home = """
[Numbers]
one=1
two=2
three=3
        """.strip()

        # first part of the tests are on home directory.
        config_in_home = self.hc.get_config_path_in_home_dir()
        # the file is expected to be missing at this point:
        self.assertFalse(os.path.isfile(config_in_home))
        # create the file in home directory:
        self.hc.create_in_home_dir(default_content=content_in_home)
        self.assertTrue(os.path.isfile(config_in_home))
        # the active config file should be the one in program directory
        self.assertEqual(self.hc.get_config_path_in_home_dir(),
                         self.hc.get_active_config_file_path())

        # get a value from the active config file.
        self.hc.get_active_config_file_path()
        config = ConfigParser.RawConfigParser()
        config.read(self.hc.get_active_config_file_path())
        self.assertEqual("2", config.get("Numbers", "two"))

        # now, switch to program directory.

        config_in_program = self.hc.get_config_path_in_program_dir()
        # the file is expected to be missing at this point:
        self.assertFalse(os.path.isfile(config_in_program))
        # create the file in program directory:
        self.hc.create_in_program_dir(default_content=content_in_program)
        self.assertTrue(os.path.isfile(config_in_program))
        # the active config file should be the one in home directory, again
        self.assertEqual(self.hc.get_config_path_in_home_dir(),
                         self.hc.get_active_config_file_path())

        # get a value from the active config file.
        # since the active config file will be the one in the home directory,
        # expected results will be the same.
        self.hc.get_active_config_file_path()
        config = ConfigParser.RawConfigParser()
        config.read(self.hc.get_active_config_file_path())
        self.assertEqual("2", config.get("Numbers", "two"))
