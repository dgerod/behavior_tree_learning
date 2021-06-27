#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import load_bt_settings, StringBehaviorTree, BehaviorNodeFactory 
from find_action.paths import EXAMPLE_DIRECTORY
from find_action.BT import behavior_tree_2 as sbt
from find_action.execution_nodes import make_execution_node


def run():

    print(sbt)

    settings_file = os.path.join(EXAMPLE_DIRECTORY, 'BT_SETTINGS.yaml')

    #   Prepare SBT: nodes and its behaviors, they shoudl be set together, there
    # are two options:
    #  1)
    #  nf.register('CHECK_picked(gear_1:gear)', Picked::make)
    #    do functionality of load_bt_settings internally
    #  nf.register('DO_move_arm_to(A:place)', MoveArmTo::make)
    #
    #  2)
    #  nf.check_exist(settings) -> raise exception if a element in sbt has not behavior in factory
    #    internally check if load_bt_settings are correct or not.
    
    load_bt_settings(settings_file)
    node_factory = BehaviorNodeFactory(make_execution_node)
    
    # Create SBT
    tree = StringBehaviorTree(sbt, behaviors=node_factory)
    tree.save_fig(EXAMPLE_DIRECTORY, name='test')

if __name__ == "__main__":
    run()
