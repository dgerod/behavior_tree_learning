import py_trees as pt
from behavior_tree_learning.sbt import BehaviorRegister, BehaviorNode, BehaviorNodeWithOperation


class CheckGearPartPicked(BehaviorNodeWithOperation):

    @staticmethod
    def make(text, world, verbose=False):
        return CheckGearPartPicked(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)
        self._world = world

    def initialise(self):
        pass

    def update(self):
        print("CheckGearPartPicked::update() [%s]" % self.name)
        success = self._world.is_gear_part_picked()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


class CheckGearPartPlaced(BehaviorNodeWithOperation):

    @staticmethod
    def make(text, world, verbose=False):
        return CheckGearPartPlaced(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)
        self._world = world

    def initialise(self):
        pass

    def update(self):
        print("CheckGearPartPlaced::update() [%s]" % self.name)
        success = self._world.is_gear_part_placed()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


class DoPickGearPart(BehaviorNodeWithOperation):

    @staticmethod
    def make(text, world, verbose=False):
        return DoPickGearPart(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)        
        self._world = world

    def initialise(self):
        pass
        
    def update(self):
        print("DoPickGearPart::update() [%s]" % self.name)
        success = self._world.pick_gear_part()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


class DoPlaceGearPart(BehaviorNodeWithOperation):

    @staticmethod
    def make(text, world, verbose=False):
        return DoPlaceGearPart(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)
        self._world = world

    def initialise(self):
        pass

    def update(self):
        print("DoPlaceGearPart::update() [%s]" % self.name)
        success = self._world.place_gear_part()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


class DoMoveGearPart(BehaviorNodeWithOperation):

    @staticmethod
    def make(text, world, verbose=False):
        return DoMoveGearPart(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)
        self._world = world

    def initialise(self):
        pass

    def update(self):
        print("DoMoveGearPart::update() [%s]" % self.name)
        success = self._world.move_gear_part()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


def get_behaviors():

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('CHECK_GearPartPlaced[]', CheckGearPartPlaced)
    behavior_register.add_condition('CHECK_GearPartPicked[]', CheckGearPartPicked)
    behavior_register.add_action('DO_PickGearPart[]', DoPickGearPart)
    behavior_register.add_action('DO_PlaceGearPart[]', DoPlaceGearPart)
    behavior_register.add_action('DO_MoveGearPart[P: place]', DoMoveGearPart)
    return behavior_register
