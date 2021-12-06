#!/usr/bin/env python3

import sys
import os

PACKAGE_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.normpath(PACKAGE_DIRECTORY))

from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister

from duplo_bt_run_example.paths import EXAMPLE_DIRECTORY
from duplo_bt_run_example import bt_collection
from duplo_bt_run_example.execution_nodes import get_behaviors
from duplo_bt_run_example import world


def run():

    node_factory = BehaviorNodeFactory(get_behaviors())

    sbt_1 = bt_collection.select_bt(0)
    sbt_2 = bt_collection.select_bt(1)
    trials = [sbt_1, sbt_2]

    start_position = [world.Pos(-0.05, -0.1, 0), world.Pos(0.0, -0.1, 0), world.Pos(0.05, -0.1, 0)]

    for tdx, trial in zip(range(0, len(trials)), trials):

        print("Trial: %d" % tdx)

        sbt = list(trial)
        print("SBT: ", sbt)

        simulated_world = world.WorldSimulator(start_position)
        bt_executor = BehaviorTreeExecutor(node_factory, simulated_world)
        success, ticks, tree = bt_executor.run(sbt, ExecutionParameters(successes_required=1))

        file_name = 'trial_%d' % (tdx + 1)
        tree.save_figure(EXAMPLE_DIRECTORY, name=file_name)
        print("Succeed: ", success)


if __name__ == "__main__":
    run()
