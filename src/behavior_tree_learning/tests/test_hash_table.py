#!/usr/bin/env python

import paths
paths.add_modules_to_path()

import unittest
from behavior_tree_learning.core.gp import hash_table


class TestHastTable(unittest.TestCase):
  
    def test_save_table_and_load(self):

        hash_table1 = hash_table.HashTable(size=10)
        hash_table1.insert(['1'], 1)
        hash_table1.insert(['2'], 2)
        hash_table1.insert(['3'], 3)
        hash_table1.insert(['4'], 4)
        hash_table1.insert(['4'], 5)
        hash_table1.write()

        hash_table2 = hash_table.HashTable(size=10)
        hash_table2.load()

        self.assertEqual(hash_table1, hash_table2)

    def test_tables_are_equal(self):

        hash_table1 = hash_table.HashTable(size=10)
        hash_table2 = hash_table.HashTable(size=10)
        hash_table1.insert(['1'], 1)
        hash_table1.insert(['2'], 2)
        hash_table2.insert(['3'], 3)
        hash_table2.insert(['4'], 4)

        self.assertEqual(hash_table1, hash_table1)
        self.assertNotEqual(hash_table1, hash_table2)
        self.assertNotEqual(hash_table1, 1)

    def test_nodes_are_equal(self):

        node1 = hash_table.Node(['a'], 1)
        node2 = hash_table.Node(['a'], 1)
        node3 = hash_table.Node(['b'], 2)
        self.assertEqual(node1, node2)
        self.assertNotEqual(node1, node3)
        self.assertNotEqual(node1, ['a'])
        self.assertNotEqual(node1, 1)

        node1.next = node3
        self.assertNotEqual(node1, node2)

        node2.next = node3
        self.assertEqual(node1, node2)

    def test_multiple_entries_in_one_table(self):

        hash_table1 = hash_table.HashTable(size=10)
        hash_table1.insert(['a'], 1)
        hash_table1.insert(['a'], 2)
        hash_table1.insert(['a'], 3)
        hash_table1.insert(['b'], 4)
        hash_table1.insert(['b'], 5)
        hash_table1.insert(['b'], 6)

        self.assertEqual(hash_table1.find(['a']), [1, 2, 3])
        self.assertEqual(hash_table1.find(['b']), [4, 5, 6])


if __name__ == '__main__':
    unittest.main()
