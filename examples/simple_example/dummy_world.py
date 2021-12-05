import collections
from interface import implements
from behavior_tree_learning.sbt import World


WorldOperationResults = \
    collections.namedtuple('WorldOperationResults', 'pick_succeed place_succeed move_succeed')


class DummyWorld(implements(World)):

    def __init__(self, operation_results: WorldOperationResults, feedback_succeed: bool = True):
        self._feedback_succeed = feedback_succeed
        self._operation_results = operation_results

    def get_feedback(self):
        return self._feedback_succeed

    def send_references(self):
        pass

    def pick_gear_part(self):
        return self._operation_results.pick_succeed

    def place_gear_part(self):
        return self._operation_results.place_succeed

    def move_gear_part(self):
        return self._operation_results.move_succeed
