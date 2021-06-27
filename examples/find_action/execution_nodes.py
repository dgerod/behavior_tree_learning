# pylint: disable=duplicate-code
"""
Implementing various py trees behaviors
For duplo brick handling in a state machine env
"""
import re
import py_trees as pt


def make_execution_node(text, world, verbose=False):

    if 'move_arm_to[A]' in text:
        node = MoveArmToPlaceA.make(text, verbose)
    else:
        node = None

    return node


class MoveArmToPlaceA(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose):
        place = re.findall(r'\[(.*?)\]', text)
        return MoveArmToPlaceA(text, world, place, verbose)

    def __init__(self, name, world, place, verbose=False):
        super(MoveArmToPlaceA, self).__init__(name)
        self._world = world
        self._place = place
        self._verbose = verbose

    def initialise(self):
        pass

    def update(self):
        pass
