#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import StringBehaviorTree
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister
from find_action.paths import EXAMPLE_DIRECTORY
from find_action.BT import behavior_tree_2 as sbt
from find_action.execution_nodes import Picked, MoveArmTo

from interface import implements
from behavior_tree_learning.core.sbt import World


class DummyWorld(implements(World)):

    def get_feedback(self):
        return True

    def send_references(self):
        pass


def run():

    print(sbt)

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('CHECK_picked[gear_1: gear]', Picked)
    behavior_register.add_action('DO_move_arm_to[A: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[B: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[C: place]', MoveArmTo)
    behavior_register.add_action('DO_move_arm_to[D: place]', MoveArmTo)
    node_factory = BehaviorNodeFactory(behavior_register)

    my_world = DummyWorld()
    tree = StringBehaviorTree(sbt, behaviors=node_factory, world=my_world)
    tree.save_figure(EXAMPLE_DIRECTORY, name='test')

    tree.run_bt()


if __name__ == "__main__":
    run()
