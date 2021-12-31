
from enum import IntEnum
from dataclasses import dataclass
from interface import implements
from behavior_tree_learning.core.sbt import World


class State(IntEnum):

    state1 = 0
    state2 = 1
    state3 = 2
    state4 = 3


@dataclass
class SMParameters:
    """Data class for parameters for the state machine simulator """
    verbose: bool = False                                  #Extra prints


class DummyWorld(implements(World)):
    """
    Class for handling the State Machine Simulator
    """

    def __init__(self):
        self.sm_par = SMParameters()
        self.state = [False]*(len(State))

    def get_feedback(self):
        # pylint: disable=no-self-use
        """ Dummy to fit template """
        return True

    def get_sensor_data(self):
        # pylint: disable=no-self-use
        """ Dummy to fit template """
        return True

    def send_references(self):
        # pylint: disable=no-self-use
        """ Dummy to fit template """
        return

    def toggle_1(self):
        self.state[State.state1] = True

    def toggle_22(self):
        self.state[State.state2] = True

    def toggle_3(self):
        self.state[State.state3] = True

    def toggle_4(self):
        self.state[State.state4] = True

    def read_1(self):
        return self.state[State.state1]

    def read_2(self):
        return self.state[State.state2]

    def read_3(self):
        return self.state[State.state3]

    def read4(self):
        return self.state[State.state4]
