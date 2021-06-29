import py_trees as pt
from behavior_tree_learning.core.sbt import behavior_tree as bt
from behavior_tree_learning.core.sbt.behaviors import RSequence


class DummyExecutionBehavior(pt.behaviour.Behaviour):

    def __init__(self, name, world, verbose):
        super().__init__(name)        

    def initialise(self):
        pass

    def update(self):
        pass
    

class BehaviorRegister:

    class BehaviorType:

        CONDITION = 1
        ACTION = 2

    def __init__(self):
        self._behaviors = {}
        
    def add_condition(self, name, behavior_class):        
        self._behaviors[name] = [self.BehaviorType.CONDITION, behavior_class]
    
    def add_action(self, name, behavior_class):        
        self._behaviors[name] = [self.BehaviorType.ACTION, behavior_class]

    def behaviors(self):
        return self._behaviors


class BehaviorNodeFactory:
    
    def __init__(self, execution_behavior_register=None):
    
        if execution_behavior_register is not None:
            self._execution_behavior_register = execution_behavior_register
            self._load_sbt_setting()
        else:
            self._execution_behavior_register = None

    def make_node(self, name, world=None, verbose=False):

        if name == 'nonpytreesbehavior':
            return None, False

        has_children = True
        node = self._make_control_node(name)
        
        if node is None and self._execution_behavior_register is not None:
        
            has_children = False
            node = self._make_execution_node(name, world, verbose)
        
            if node is None:
                raise Exception("Unexpected character", name)

        return node, has_children

    def _load_sbt_setting(self):

        bt.add_node('fallback', 'f(')
        bt.add_node('sequence', 's(')

        behaviors = self._execution_behavior_register.behaviors()
        for key in behaviors.keys():

            if behaviors[key][0] == BehaviorRegister.BehaviorType.CONDITION:
                type_ = 'condition'    
            elif behaviors[key][0] == BehaviorRegister.BehaviorType.ACTION:
                type_ = 'action'    
            
            name = key
            bt.add_node(type_, name)

    def _make_control_node(self, name):
        
        node = None

        if name == 'f(':
            node = pt.composites.Selector('Fallback')
        elif name == 's(':
            node = RSequence()
        elif name == 'p(':
            node = pt.composites.Parallel(name="Parallel",
                                          policy=pt.common.ParallelPolicy.SuccessOnAll(synchronise=False))

        return node

    def _make_execution_node(self, name, world, verbose):

        behaviors = self._execution_behavior_register.behaviors()
        for key in behaviors.keys():
            if name in key:
                return behaviors[key][1].make(name, world, verbose)
        
        return None


def make_factory_from_file(file_path):
    return NotImplementedError
