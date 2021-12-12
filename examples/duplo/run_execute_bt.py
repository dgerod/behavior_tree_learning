#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import BehaviorNodeFactory

from duplo.paths import get_log_directory
from duplo import bt_collection
from duplo.execution_nodes import get_behaviors
from duplo.world import WorldSimulator
from duplo.world import Pos as WorldPos


def run():

    node_factory = BehaviorNodeFactory(get_behaviors('tower'))

    sbt_1 = bt_collection.select_bt(0)
    sbt_2 = bt_collection.select_bt(1)
    trials = [sbt_1, sbt_2]

    start_position = [WorldPos(-0.05, -0.1, 0), WorldPos(0.0, -0.1, 0), WorldPos(0.05, -0.1, 0)]

    for tdx, trial in zip(range(1, len(trials)+1), trials):

        print("Trial: %d" % tdx)

        sbt = list(trial)
        print("SBT: ", sbt)

        simulated_world = WorldSimulator(start_position)
        bt_executor = BehaviorTreeExecutor(node_factory, simulated_world)

        success, ticks, tree = bt_executor.run(sbt, ExecutionParameters(successes_required=1),
                                               verbose=True)

        try:
            os.mkdir(get_log_directory())
        except OSError:
            pass

        file_name = 'trial_%d' % (tdx + 1)
        tree.save_figure(get_log_directory(), name=file_name)
        print("Succeed: ", success)


if __name__ == "__main__":
    run()
