#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

import os
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorTreeExecutor, ExecutionParameters
from tiago_pnp.paths import get_log_directory
from tiago_pnp import bt_collection
from tiago_pnp.execution_nodes import get_behaviors
from tiago_pnp.world import WorldSimulator


def run():

    scenario = 'scenario_1'
    deterministic = False

    node_factory_1 = BehaviorNodeFactory(get_behaviors(scenario))
    sbt_1 = bt_collection.select_bt(scenario)
    trials = [(sbt_1, node_factory_1)]

    for tdx, trial in zip(range(0, len(trials)), trials):

        print("Trial: %d" % tdx)

        sbt = list(trial[0])
        node_factory = trial[1]
        print("SBT: ", sbt)

        simulated_world = WorldSimulator(scenario, deterministic)
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
