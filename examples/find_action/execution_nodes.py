# pylint: disable=duplicate-code
"""
Implementing various py trees behaviors
For duplo brick handling in a state machine env
"""
import re
import py_trees as pt
from find_action.parse_operation import parse_function, print_parsed_function

def make_execution_node(text, world, verbose=False):

    if 'CHECK_picked' in text:
        node = Picked.make(text, verbose)
    elif 'DO_move_arm_to' in text:
        node = MoveArmTo.make(text, verbose)
    else:
        node = None

    return node


class Picked(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):

        print_parsed_function(text)        
        name, arguments, return_value = parse_function(text)      

        text_2 = name + " " + str(arguments) + " => " + str(return_value)               
        return Picked(text_2, world, verbose)

    def __init__(self, name, world, verbose):
        
        super().__init__(name)             
        self._world = world
        self._verbose = verbose

    def initialise(self):
        print("Picked::initialise() [%s]", self.name)

    def update(self):
        print("Picked::update() [%s]", self.name)
        return pt.common.Status.SUCCESS


class MoveArmTo(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):
        
        print_parsed_function(text)        
        name, arguments, return_value = parse_function(text)             
        
        #place = re.findall(r'\[(.*?)\]', text)
        place = ""

        text_2 = name + " " + str(arguments) + " => " + str(return_value)

        # Retrieve place from SDB
        return MoveArmTo(text_2, world, place, verbose)

    def __init__(self, name, world, place, verbose):
        
        super().__init__(name)        
        self._world = world
        self._place = place
        self._verbose = verbose

    def initialise(self):
        print("MoveArmTo::initialise() [%s]", self.name)

    def update(self):
        print("MoveArmTo::update() [%s]", self.name)
        return pt.common.Status.SUCCESS
