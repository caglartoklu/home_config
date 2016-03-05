#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A library to facilitate automatic config file creation in the home directory.

To install:
pip install home_config
"""

# pylint: disable=C0103
# Disables:
# Invalid module name "atom-linter_xxxxxx"at
# line 1 col 1 in dropshadow_bed\__init__.py
# This warning occurs in in linter-pylint extension of Atom.


from __future__ import print_function
from __future__ import unicode_literals
import sys
import os.path


class HomeConfigFileNotFoundError(OSError):
    """Raised when the config file is not found."""

    def __init__(self, message):
        """Initialize an instance of HomeConfigFileNotFoundError."""
        super(HomeConfigFileNotFoundError, self).__init__(message)


class HomeConfigFileAlreadyFoundError(OSError):
    """Raised when a file is to be created but it already exists."""
    def __init__(self, message):
        """Initialize an instance of HomeConfigFileAlreadyFoundError."""
        super(HomeConfigFileAlreadyFoundError, self).__init__(message)


def _get_home_dir():
    """Return the path to the home directory of the user."""
    return os.path.expanduser("~")


def _get_program_dir():
    """
    Return the path to the program directory.

    That is the directory of the executing script.
    """
    return os.path.abspath(os.path.dirname(sys.argv[0]))


def _get_module_dir():
    """Return the path of the module."""
    return os.path.abspath(os.path.dirname(__file__))


def _write_file(file_name, content, forced=False):
    """
    Create a file in the specified directory.

    If the file does not exist, it will be created.
    If forced==False and the file exists, it will raise an error.
    If forced==True and the file exists, the file will be overwritten.
    """
    if os.path.isfile(file_name) and not forced:
        # file exists and forced is False,
        # raise an exception.
        message = "File already exists, use forced=True : "
        message += file_name
        raise HomeConfigFileAlreadyFoundError(message)
    else:
        # file does not exist or it can be overwritten.
        file_handle = open(file_name, "w")
        file_handle.write(content)
        file_handle.close()


class HomeConfig(object):
    """Encapsulates the config file facilities."""

    def __init__(self, config_file_name,
                 program_dir=None, home_dir=None):
        """
        Initialize an instance of HomeConfig class.

        config_file_name: string
            Only the file name of the config file.
        program_dir: string
            The program directory if specified.
            Otherwise, it will be auto detected.
            This parameter is useful when the script is bundled in a executable
            packer, or run from a temp directory.
        home_dir: string
            The home directory of the user if specified.
            Otherwise, it will be auto detected.
            It is advised to leave this option for auto detection.
        """
        self._config_file_name = config_file_name
        if program_dir is None:
            self._program_dir = _get_program_dir()
        else:
            self._program_dir = program_dir

        if home_dir is None:
            self._home_dir = _get_home_dir()
        else:
            self._home_dir = home_dir

    def get_config_file_name(self):
        """
        Return the config file name.

        Not the full path, only the file name itself.
        """
        return self._config_file_name

    def get_program_dir(self):
        """
        Return the program directory.

        This is the directory that includes the executable.
        """
        return self._program_dir

    def get_home_dir(self):
        """
        Return the home directory.

        This is the directory of the user, its home directory.
        """
        return self._home_dir

    def get_config_path_in_home_dir(self):
        """
        Return the full path to the config file in the home directory.

        This function will return a value whether the file exists or not.
        """
        result = os.path.join(self.get_home_dir(),
                              self._config_file_name)
        result = os.path.abspath(result)
        return result

    def get_config_path_in_program_dir(self):
        """
        Return the full path to the config file in the program directory.

        This function will return a value whether the file exists or not.
        """
        result = os.path.join(self.get_program_dir(),
                              self._config_file_name)
        result = os.path.abspath(result)
        return result

    def create_in_home_dir(self, default_content, forced=False):
        """
        Create the config file in the home directory.

        If the file does not exist, it will be created.
        If forced==False and the file exists, it will raise an error.
        If forced==True and the file exists, the file will be overwritten.
        """
        file_name = self.get_config_path_in_home_dir()
        print(file_name)
        _write_file(file_name=file_name,
                    content=default_content, forced=forced)

    def create_in_program_dir(self, default_content, forced=False):
        """
        Create the config file in the program directory.

        If the file does not exist, it will be created.
        If forced==False and the file exists, it will raise an error.
        If forced==True and the file exists, the file will be overwritten.
        """
        file_name = self.get_config_path_in_program_dir()
        _write_file(file_name=file_name,
                    content=default_content, forced=forced)

    def get_active_config_file_path(self):
        """
        Return the path to the active config file.

        The one in the home directory is more dominant than the one in the
        program directory.

        If no config file can be detected, this function will raise:
            HomeConfigFileNotFoundError
        """
        config_file_name = ""
        candidate_file_name = self.get_config_path_in_home_dir()
        if os.path.isfile(candidate_file_name):
            # check a config file in home directory first.
            config_file_name = candidate_file_name
        else:
            # a config file not found in home directory.
            # check a config file in program directory then.
            candidate_file_name = self.get_config_path_in_program_dir()
            if os.path.isfile(candidate_file_name):
                config_file_name = candidate_file_name

        if len(config_file_name) > 0:
            return config_file_name
        else:
            message = "File not found : " + str(config_file_name)
            raise HomeConfigFileNotFoundError(message)


def _main():
    """entry point of the module."""
    pass

if __name__ == '__main__':
    _main()
