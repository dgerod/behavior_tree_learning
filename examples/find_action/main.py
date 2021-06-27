#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import BehaviorNodeFactory
from behavior_tree_learning.sbt import StringBehaviorTree
from find_action.BT import behavior_tree as sbt
from find_action.execution_nodes import make_execution_node

def run():

    print(sbt)

    node_factory = BehaviorNodeFactory(make_execution_node)
    behavior_tree = StringBehaviorTree(sbt, behaviors=node_factory)

if __name__ == "__main__":
    run()
