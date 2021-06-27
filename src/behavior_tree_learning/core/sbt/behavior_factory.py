import py_trees as pt
from behavior_tree_learning.core.sbt.behaviors import RSequence


class BehaviorNodeFactory:
    
    def __init__(self, make_execution_node):
        self._make_execution_node = make_execution_node

    def make_node(self, text, world, verbose=False):

        if text == 'nonpytreesbehavior':
            return None, False

        has_children = True
        node = self._make_control_node(text)
        
        if node is None:
        
            has_children = False
            node = self._make_execution_node(text, world, verbose)
        
            if node is None:
                raise Exception("Unexpected character", text)

        return node, has_children

    def _make_control_node(text):
        
        node = None

        if text == 'f(':
            node = pt.composites.Selector('Fallback')
        elif text == 's(':
            node = RSequence()
        elif text == 'p(':
            node = pt.composites.Parallel(
                name="Parallel",
                policy=pt.common.ParallelPolicy.SuccessOnAll(synchronise=False))

        return node
