from behavior_tree_learning.core.sbt.behavior_factory import BehaviorNodeFactory
from behavior_tree_learning.core.sbt.py_tree import StringBehaviorTree, ExecutionParameters
from behavior_tree_learning.core.sbt.world import World


class BehaviorTreeExecutor:

    def __init__(self, node_factory: BehaviorNodeFactory, world: World):
        self._node_factory = node_factory
        self._world = world

    def run(self, sbt: str, parameters: ExecutionParameters):
        tree = StringBehaviorTree(sbt, behaviors=self._node_factory, world=self._world)
        ticks, success = tree.run_bt(parameters=parameters)
        return success, ticks, tree
