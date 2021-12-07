import collections
from interface import implements
from behavior_tree_learning.sbt import World


WorldOperationResults = \
    collections.namedtuple('WorldOperationResults',
                           'is_picked_succeed is_placed_succeed do_pick_succeed do_place_succeed do_move_succeed')


class DummyWorld(implements(World)):

    def __init__(self, operation_results: WorldOperationResults, is_alive: bool = True):
        self._is_alive = is_alive
        self._operation_results = operation_results

    def get_feedback(self):
        return self._is_alive

    def startup(self):
        return True

    def is_alive(self):
        return self._is_alive

    def shutdown(self):
        pass

    def is_gear_part_picked(self):
        return self._operation_results.is_picked_succeed

    def is_gear_part_placed(self):
        return self._operation_results.is_placed_succeed

    def pick_gear_part(self):
        return self._operation_results.do_pick_succeed

    def place_gear_part(self):
        return self._operation_results.do_place_succeed

    def move_gear_part(self):
        return self._operation_results.do_move_succeed
