import py_trees as pt
from behavior_tree_learning.core.sbt.behavior_factory import BehaviorNodeFactory


class PlannerBehaviorNodeFactory:
    
    def __init__(self, make_execution_node, get_condition_parameters):

        self._behavior_factory = BehaviorNodeFactory(make_execution_node)
        self._make_execution_node = make_execution_node
        self._get_condition_parameters = get_condition_parameters

    def get_condition_parameters(self, condition):
        
        return self._get_condition_parameters(condition)

    def get_node(self, name: str, world, condition_parameters):
        
        node = self._behavior_factory.make_node(name)

        if node is None:
            return self._make_execution_node(name, world, condition_parameters)
        else:
            return node, True
