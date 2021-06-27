import py_trees as pt
from behavior_tree_learning.core.sbt.behaviors import RSequence


class BehaviorNodeFactory:
    
    def __init__(self, make_execution_node=None):
        self._make_execution_node = make_execution_node

    def make_node(self, name, world=None, verbose=False):

        if name == 'nonpytreesbehavior':
            return None, False

        has_children = True
        node = self._make_control_node(name)
        
        if node is None and self._make_execution_node is not None:
        
            has_children = False
            node = self._make_execution_node(name, world, verbose)
        
            if node is None:
                raise Exception("Unexpected character", name)

        return node, has_children

    def _make_control_node(self, name):
        
        node = None

        if name == 'f(':
            node = pt.composites.Selector('Fallback')
        elif name == 's(':
            node = RSequence()
        elif name == 'p(':
            node = pt.composites.Parallel(
                name="Parallel",
                policy=pt.common.ParallelPolicy.SuccessOnAll(synchronise=False))

        return node
