import os
import sys


_this_file_path = os.path.abspath(__file__)
_PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(_this_file_path)))
_EXAMPLES_DIRECTORY = os.path.dirname(os.path.dirname(_this_file_path))
_CURRENT_EXAMPLE_DIRECTORY = os.path.dirname(_this_file_path)


def add_modules_to_path():
    sys.path.append(os.path.normpath(_PACKAGE_DIRECTORY))
    sys.path.append(os.path.normpath(_EXAMPLES_DIRECTORY))


def get_example_directory():
    return _CURRENT_EXAMPLE_DIRECTORY


def get_outputs_directory():
    return os.path.join(_CURRENT_EXAMPLE_DIRECTORY, 'results')
