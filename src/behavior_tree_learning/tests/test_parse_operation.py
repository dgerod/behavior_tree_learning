#!/usr/bin/env python3

import os
import sys

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

import unittest
from behavior_tree_learning.core.sbt.parse_operation import parse_function


class TestParseFunctionAsText(unittest.TestCase):

    @staticmethod
    def _execute_test(test_name, text):

        print("\n")
        print(test_name)
        print(" + original: ", text)
        name, arguments, return_value = parse_function(text)
        print(" + Result")
        print("    + name: ", name)
        print("    + arguments: ", arguments)
        print("    + return value: ", return_value)

    def test_correct_syntax_using_without_arguments_1(self):

        text = "a_function[] => [E :bool]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "a_function")
        self.assertEqual(arguments, None)
        self.assertEqual(return_value, {'E': 'bool'})

    def test_correct_syntax_using_without_arguments_2(self):

        text = "a_function []=>[E :bool]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "a_function")
        self.assertEqual(arguments, None)
        self.assertEqual(return_value, {'E': 'bool'})

    def test_correct_syntax_using_one_argument(self):

        text = "another_function[A :place] => [E :bool]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "another_function")
        self.assertEqual(arguments, {'A': 'place'})
        self.assertEqual(return_value, {'E': 'bool'})

    def test_correct_syntax_using_two_argument(self):

        text = "another_function[A:place, B :pose]=>[E :bool]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "another_function")
        self.assertEqual(arguments, {'A': 'place', 'B': 'pose'})
        self.assertEqual(return_value, {'E': 'bool'})

    def test_correct_syntax_without_return_value_1(self):
        text = "another_function[]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "another_function")
        self.assertEqual(arguments, None)
        self.assertEqual(return_value, None)

    def test_correct_syntax_without_return_value_2(self):

        text = "another_function[A:place]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "another_function")
        self.assertEqual(arguments, {'A': 'place'})
        self.assertEqual(return_value, None)

    def test_correct_syntax_without_return_value_3(self):

        text = "another_function[A:place, B :pose]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "another_function")
        self.assertEqual(arguments, {'A': 'place', 'B': 'pose'})
        self.assertEqual(return_value, None)

    def test_correct_syntax_with_two_return_values(self):

        text = "another_function[] => [E :bool, F:place]"
        name, arguments, return_value = parse_function(text)

        self.assertEqual(name, "another_function")
        self.assertEqual(arguments, None)
        self.assertEqual(return_value, {'E': 'bool', 'F': 'place'})

    def test_wrong_syntax_return_value_without_parenthesis(self):

        with self.assertRaises(Exception):
            text = "another_function[] => E :bool"
            parse_function(text)

    def test_wrong_syntax_function_declaration_without_parenthesis(self):

        with self.assertRaises(Exception):
            text = "another_function => (E :bool)"
            parse_function(text)

    def test_wrong_syntax_return_values_only_parenthesis(self):

        with self.assertRaises(Exception):
            text = "another_function[] => []"
            parse_function(text)


if __name__ == '__main__':
    unittest.main()
