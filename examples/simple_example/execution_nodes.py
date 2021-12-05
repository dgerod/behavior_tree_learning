import py_trees as pt


class PickGearPart(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):
        return PickGearPart(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)        
        self._world = world

    def initialise(self):
        print("PickGearPart::initialise() [%s]" % self.name)
        
    def update(self):
        print("PickGearPart::update() [%s]" % self.name)
        success = self._world.pick_gear_part()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


class PlaceGearPart(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):
        return PlaceGearPart(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)
        self._world = world

    def initialise(self):
        print("PlaceGearPart::initialise() [%s]" % self.name)

    def update(self):
        print("PlaceGearPart::update() [%s]" % self.name)
        success = self._world.place_gear_part()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE


class MoveGearPart(pt.behaviour.Behaviour):

    @staticmethod
    def make(text, world, verbose=False):
        return MoveGearPart(text, world, verbose)

    def __init__(self, name, world, verbose):
        super().__init__(name)
        self._world = world

    def initialise(self):
        print("MoveGearPart::initialise() [%s]" % self.name)

    def update(self):
        print("MoveGearPart::update() [%s]" % self.name)
        success = self._world.move_gear_part()
        return pt.common.Status.SUCCESS if success else pt.common.Status.FAILURE
