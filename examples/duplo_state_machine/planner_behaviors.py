"""
Behaviors for automated planner.
Only difference is that pre and postconditions are added.
"""
import re
import py_trees as pt

from behavior_tree_learning.learning import RSequence
from duplo_state_machine import behaviors
from duplo_state_machine import state_machine as sm


def get_node_from_string(string, world, condition_parameters):
    # pylint: disable=too-many-branches
    """
    Returns a py trees behavior or composite given the string
    """

    has_children = False
    if 'pick ' in string:
        node = Pick(string, world, re.findall(r'\d+', string), condition_parameters)
    elif 'place at' in string:
        node = PlaceAt(string, world, re.findall(r'-?\d+\.\d+|-?\d+', string), condition_parameters)
    elif 'place on' in string:
        node = PlaceOn(string, world, re.findall(r'\d+', string), condition_parameters)
    elif 'put' in string and 'at' in string:
        node = PutAt(string, world, re.findall(r'-?\d+\.\d+|-?\d+', string), condition_parameters)
    elif 'put' in string and 'on' in string:
        node = PutOn(string, world, re.findall(r'\d+', string), condition_parameters)
    elif 'apply force' in string:
        node = ApplyForce(string, world, re.findall(r'\d+', string), condition_parameters)
    elif 'picked ' in string:
        node = Picked(string, world, re.findall(r'\d+', string), condition_parameters)
    elif 'hand empty' in string:
        node = HandEmpty(string, world, condition_parameters)
    elif 'at pos ' in string:
        node = AtPos(string, world, re.findall(r'-?\d+\.\d+|-?\d+', string), condition_parameters)
    elif string == 'f(':
        node = pt.composites.Selector('Fallback')
        has_children = True
    elif string == 's(':
        node = RSequence()
        has_children = True
    elif string == 'p(':
        node = pt.composites.Parallel(
            name="Parallel",
            policy=pt.common.ParallelPolicy.SuccessOnAll(synchronise=False))
        has_children = True
    else:
        raise Exception("Unexpected character", string)

    return node, has_children


def get_condition_parameters(condition):
    """
    Returns a list of parameters associated with the condition entered
    """
    if 'picked ' in condition:
        return re.findall(r'\d+', condition)
    if 'at pos ' in condition:
        return re.findall(r'\d+\.\d+|\d+', condition)
    if ' on ' in condition:
        return re.findall(r'\d+', condition)

    return []


def get_position_string(position):
    """ Returns a string of the position for creating behavior names """
    return '(' + str(position[0]) + ', ' + str(position[1]) + ', ' + str(position[2]) + ')'


class PlannedBehavior():
    """
    Class template for planned behaviors
    """
    def __init__(self, preconditions, postconditions):
        self.preconditions = preconditions
        self.postconditions = postconditions

    def get_preconditions(self):
        """ Returns list of preconditions """
        return self.preconditions

    def get_postconditions(self):
        """ Returns list of postconditions """
        return self.postconditions


class HandEmpty(behaviors.HandEmpty, PlannedBehavior):
    """
    Check if hand is empty
    """
    def __init__(self, name, world, _condition_parameters):
        behaviors.HandEmpty.__init__(self, name, world)
        PlannedBehavior.__init__(self, [], [])


class Picked(behaviors.Picked, PlannedBehavior):
    """
    Check if brick is picked
    """
    def __init__(self, name, world, brick, _condition_parameters):
        behaviors.Picked.__init__(self, name, world, brick)
        PlannedBehavior.__init__(self, [], [])


class AtPos(behaviors.AtPos, PlannedBehavior):
    """
    Check if brick is at goal
    """
    def __init__(self, name, world, brick_and_pos, _condition_parameters):
        behaviors.AtPos.__init__(self, name, world, brick_and_pos)
        PlannedBehavior.__init__(self, [], [])


class On(behaviors.On, PlannedBehavior):
    """
    Check if brick is at goal
    """
    def __init__(self, name, world, bricks, _condition_parameters):
        behaviors.On.__init__(self, name, world, bricks)
        PlannedBehavior.__init__(self, [], [])


class Pick(behaviors.Pick, PlannedBehavior):
    """
    Pick up a brick
    """
    def __init__(self, name, world, brick, _condition_parameters):
        behaviors.Pick.__init__(self, name, world, brick)
        PlannedBehavior.__init__(self, [], ['picked ' + str(brick[0]) + '?'])


class PlaceAt(behaviors.Place, PlannedBehavior):
    """
    Place given brick at given position
    """
    def __init__(self, name, world, position, condition_parameters):
        behaviors.Place.__init__(self, name, world, position=position)
        PlannedBehavior.__init__(self, ['picked ' + str(condition_parameters[0]) +  '?'], \
            ['hand empty?', str(condition_parameters[0]) + ' at pos ' + get_position_string(position) + '?'])


class PlaceOn(behaviors.Place, PlannedBehavior):
    """
    Place current brick on other given brick
    """
    def __init__(self, name, world, brick, condition_parameters):
        behaviors.Place.__init__(self, name, world, brick=brick)
        PlannedBehavior.__init__(self, ['picked ' + str(condition_parameters[0]) +  '?'], ['hand empty?'])
        self.condition_parameters = condition_parameters

    def get_postconditions(self):
        """
        This one is a bit special because the postcondition
        will depend on current state of the other brick
        """
        brickpos = [str(self.condition_parameters[0]) + ' on ' + str(self.brick) + '?']
        return self.postconditions + brickpos


class PutAt(behaviors.Put, PlannedBehavior):
    """
    Picks brick and places it at position
    """
    def __init__(self, name, world, brick_and_pos, _condition_parameters):
        behaviors.Put.__init__(self, name, world, brick_and_pos)
        PlannedBehavior.__init__(self, [], \
                                 [str(brick_and_pos[0]) + ' at pos ' + get_position_string(brick_and_pos[1:]) + '?'])


class PutOn(behaviors.Put, PlannedBehavior):
    """
    Picks brick and places it on other brick
    """
    def __init__(self, name, world, brick_and_pos, condition_parameters):
        behaviors.Put.__init__(self, name, world, brick_and_pos)
        PlannedBehavior.__init__(self, [], [str(self.brick) + ' on ' + str(self.lower) + '?'])
        self.condition_parameters = condition_parameters


class ApplyForce(behaviors.ApplyForce, PlannedBehavior):
    """
    Apply force on given brick
    A bit of a cheaty implementation of pre and postconditions here to handle our experiments,
    but we are only using it to create a result that some planner theoretically could generate
    """
    def __init__(self, name, world, brick, _condition_parameters):
        behaviors.ApplyForce.__init__(self, name, world, brick)
        PlannedBehavior.__init__(self, [], [])

    def get_preconditions(self):
        if self.brick == 0:
            return ['1 at pos (0.0, 0.0, 0.0)?', '0 on 1?']
        if self.brick == 1:
            return ['1 on 0?']
        if self.brick == 2:
            return ['2 on 1?']
        return self.preconditions

    def get_postconditions(self):
        if self.brick > 0:
            brickpos = self.world.state.bricks[self.brick - 1] + \
                sm.Pos(0, 0, self.world.sm_par.brick_height)
            self.postconditions = [str(self.brick) + ' at pos ' + str(brickpos) + '?']
        else:
            brickpos = sm.Pos(0.0, 0.0, self.world.sm_par.brick_height)
            self.postconditions = [str(self.brick) + ' at pos ' + str(brickpos) + '?']
        return self.postconditions
