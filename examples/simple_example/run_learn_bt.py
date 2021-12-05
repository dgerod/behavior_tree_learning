#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister

from find_action.paths import EXAMPLE_DIRECTORY
from find_action.behavior_trees import select_bt
from find_action.execution_nodes import PickGearPart, PlaceGearPart, MoveGearPart
from find_action.dummy_world import DummyWorld


def run():

    sbt = select_bt(2)
    print("SBT: ", sbt)

    behavior_register = BehaviorRegister()
    behavior_register.add_action('PickGearPart', PickGearPart)
    behavior_register.add_action('PlaceGearPart', PlaceGearPart)
    behavior_register.add_action('MoveGearPart', MoveGearPart)

    node_factory = BehaviorNodeFactory(behavior_register)
    my_world = DummyWorld()

    bt_executor = BehaviorTreeExecutor(node_factory, my_world)
    success, ticks, tree = bt_executor.run(sbt, ExecutionParameters(successes_required=1))
    tree.save_figure(EXAMPLE_DIRECTORY, name='test')

    print("Succeed: ", success)


if __name__ == "__main__":
    run()
