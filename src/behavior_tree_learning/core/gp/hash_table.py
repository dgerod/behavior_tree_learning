"""
Hash table with linked list for entries with same hash
"""

import os
import hashlib
import ast

import behavior_tree_learning.core.logger.logplot as logplot


class Node:
    """
    Node data structure - essentially a LinkedList node
    """

    def __init__(self, key, value):
        self.key = key
        self.value = [value]
        self.next = None

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        equal = self.key == other.key and self.value == other.value
        if equal:
            if self.next is not None or other.next is not None:
                if self.next is None or other.next is None:
                    equal = False
                else:
                    equal = self.next == other.next
        return equal


class HashTable:

    _FILE_NAME = 'hash_log.txt'
    _DEFAULT_LOG_NAME = 'test'

    def __init__(self, size=100000, name: str = ''):
        """_
        Initialize hash table to fixed size
        """

        self.size = size
        self.file_name = self._DEFAULT_LOG_NAME if name == '' else name
        self.buckets = [None]*self.size
        self.n_values = 0

    def __eq__(self, other):

        if not isinstance(other, HashTable):
            return False

        equal = True
        for i in range(self.size):
            if self.buckets[i] != other.buckets[i]:
                equal = False
                break
        return equal

    def hash(self, key: str):
        """
        Generate a hash for a given key
        Input:  string key
        Output: hash
        """

        string = ''.join(key)
        new_hash = hashlib.md5()
        new_hash.update(string.encode('utf-8'))
        hashcode = new_hash.hexdigest()
        hashcode = int(hashcode, 16)
        return hashcode % self.size

    def insert(self, key: str, value):
        """
        Insert a key - value pair to the hashtable
        Input:  key - string
                value - anything
        """

        index = self.hash(key)
        node = self.buckets[index]
        if node is None:
            self.buckets[index] = Node(key, value)
        else:
            done = False
            while not done:
                if node.key == key:
                    node.value.append(value)
                    done = True
                elif node.next is None:
                    node.next = Node(key, value)
                    done = True
                else:
                    node = node.next

        self.n_values += 1

    def find(self, key: str):
        """
        Find a data value based on key
        Input:  key - string
        Output: value stored under "key" or None if not found
        """

        index = self.hash(key)
        node = self.buckets[index]
        while node is not None and node.key != key:
            node = node.next

        if node is None:
            return None
        return node.value

    def load(self):
        """
        Loads hash table information.
        """

        file_name = os.path.join(logplot.get_log_folder(self.file_name), self._FILE_NAME)
        with open(file_name, 'r') as f:
            lines = f.read().splitlines()

            for i in range(0, len(lines)):
                individual = lines[i]
                individual = individual[5:].split(', value: ')
                key = ast.literal_eval(individual[0])
                individual = individual[1].split(', count: ')
                values = individual[0][1:-1].split(', ')  # Remove brackets and split multiples
                for value in values:
                    self.insert(key, float(value))

    def write(self):
        """
        Writes table contents to a file
        """

        file_name = os.path.join(logplot.get_log_folder(self.file_name), self._FILE_NAME)

        with open(file_name, 'w') as f:
            for node in filter(lambda x: x is not None, self.buckets):
                while node is not None:
                    f.writelines('key: ' + str(node.key) +
                                 ', value: ' + str(node.value) +
                                 ', count: ' + str(len(node.value)) + '\n')
                    node = node.next
        f.close()
