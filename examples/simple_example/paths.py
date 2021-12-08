import os
import sys


_this_file_path = os.path.abspath(__file__)
_PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(_this_file_path)))
_EXAMPLE_DIRECTORY = os.path.dirname(os.path.dirname(_this_file_path))


def add_modules_to_path():
    sys.path.append(os.path.normpath(_PACKAGE_DIRECTORY))
    sys.path.append(os.path.normpath(_EXAMPLE_DIRECTORY))


def get_example_directory():
    return _EXAMPLE_DIRECTORY
