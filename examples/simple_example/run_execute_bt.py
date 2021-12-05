#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister

from simple_example.paths import EXAMPLE_DIRECTORY
from simple_example import bt_collection
from simple_example.execution_nodes import PickGearPart, PlaceGearPart, MoveGearPart
from simple_example.dummy_world import DummyWorld, WorldOperationResults


def run():

    behavior_register = BehaviorRegister()
    behavior_register.add_action('PickGearPart', PickGearPart)
    behavior_register.add_action('PlaceGearPart', PlaceGearPart)
    behavior_register.add_action('MoveGearPart', MoveGearPart)

    node_factory = BehaviorNodeFactory(behavior_register)

    sbt_1 = bt_collection.select_bt(0)
    sbt_2 = bt_collection.select_bt(1)
    trials = [(sbt_1, WorldOperationResults(pick_succeed=True, place_succeed=True, move_succeed=True)),
              (sbt_1, WorldOperationResults(pick_succeed=False, place_succeed=False, move_succeed=False)),
              (sbt_2, WorldOperationResults(pick_succeed=True, place_succeed=True, move_succeed=True)),
              (sbt_2, WorldOperationResults(pick_succeed=False, place_succeed=False, move_succeed=False))]
    world_feedback_succeed = True

    for tdx, trial in zip(range(0, len(trials)), trials):

        print("Trial: %d" % tdx)

        sbt = list(trial[0])
        world_operations = trial[1]

        print("SBT: ", sbt)
        print("World operations: ", world_operations)

        world = DummyWorld(world_operations, world_feedback_succeed)
        bt_executor = BehaviorTreeExecutor(node_factory, world)
        success, ticks, tree = bt_executor.run(sbt, ExecutionParameters(successes_required=1))

        file_name = 'trial_%d' % (tdx + 1)
        tree.save_figure(EXAMPLE_DIRECTORY, name=file_name)
        print("Succeed: ", success)


if __name__ == "__main__":
    run()
