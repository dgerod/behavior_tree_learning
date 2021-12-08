#!/usr/bin/env python3

import paths
paths.add_modules_to_path()

from behavior_tree_learning.sbt import BehaviorTreeExecutor, ExecutionParameters
from behavior_tree_learning.sbt import BehaviorNodeFactory, BehaviorRegister

from simple_example.paths import get_example_directory
from simple_example import bt_collection
from simple_example.execution_nodes import get_behaviors
from simple_example.dummy_world import DummyWorld, WorldOperationResults


def run():

    node_factory = BehaviorNodeFactory(get_behaviors())

    sbt_1 = bt_collection.select_bt(0)
    sbt_2 = bt_collection.select_bt(1)
    trials = [(sbt_1, WorldOperationResults(is_picked_succeed=True, is_placed_succeed=True,
                                            do_pick_succeed=True, do_place_succeed=True, do_move_succeed=True)),
              (sbt_1, WorldOperationResults(is_picked_succeed=False, is_placed_succeed=False,
                                            do_pick_succeed=False, do_place_succeed=False, do_move_succeed=False)),
              (sbt_2, WorldOperationResults(is_picked_succeed=True, is_placed_succeed=True,
                                            do_pick_succeed=True, do_place_succeed=True, do_move_succeed=True)),
              (sbt_2, WorldOperationResults(is_picked_succeed=False, is_placed_succeed=False,
                                            do_pick_succeed=False, do_place_succeed=False, do_move_succeed=False))]
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
        tree.save_figure(get_example_directory(), name=file_name)
        print("Succeed: ", success)


if __name__ == "__main__":
    run()
