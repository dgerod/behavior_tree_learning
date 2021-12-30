import os
import sys


_this_file_path = os.path.abspath(__file__)
_PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(_this_file_path))
_TEST_DIRECTORY = os.path.dirname(_this_file_path)


def add_modules_to_path():
    sys.path.append(os.path.normpath(_PACKAGE_DIRECTORY))


def get_test_directory():
    return _TEST_DIRECTORY


def get_log_directory():
    return os.path.join(_TEST_DIRECTORY, 'logs')
