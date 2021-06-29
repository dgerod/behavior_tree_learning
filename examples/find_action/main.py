#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import load_bt_settings, StringBehaviorTree, BehaviorNodeFactory 
from find_action.paths import EXAMPLE_DIRECTORY
from find_action.BT import behavior_tree_2 as sbt
from find_action.execution_nodes import make_execution_node

from behavior_tree_learning.core.sbt.behavior_factory import BehaviorRegister
from find_action.execution_nodes import Picked, MoveArmTo


def run():

    print(sbt)

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('CHECK_picked[gear_1: gear]', Picked)
    behavior_register.add_action('DO_move_arm_to[A: place]', MoveArmToA)
    behavior_register.add_action('DO_move_arm_to[B: place]', MoveArmToB)
    behavior_register.add_action('DO_move_arm_to[C: place]', MoveArmToC)
    behavior_register.add_action('DO_move_arm_to[D: place]', MoveArmToD)
    node_factory = BehaviorNodeFactory(behavior_register)

    tree = StringBehaviorTree(sbt, behaviors=node_factory)
    tree.save_fig(EXAMPLE_DIRECTORY, name='test')

    tree.bt


if __name__ == "__main__":
    run()
