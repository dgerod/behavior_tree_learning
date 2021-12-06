import re
import py_trees as pt
from behavior_tree_learning.sbt import BehaviorRegister, BehaviorNode
import duplo_bt_run_example.world as sm


_behavior_register = None


class HandEmpty(BehaviorNode):
    """
    Check if hand is empty
    """

    @staticmethod
    def make(text, world, verbose=False):
        return HandEmpty(text, world)

    def __init__(self, name, world):
        self._world = world
        super(HandEmpty, self).__init__(name)

    def update(self):
        if self._world.hand_empty():
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class Picked(BehaviorNode):
    """
    Check if brick is picked
    """

    @staticmethod
    def make(text, world, verbose=False):
        return Picked(text, world, re.findall(r'\d+', text))

    def __init__(self, name, world, brick):
        self._world = world
        self._brick = int(brick[0])
        super(Picked, self).__init__(name)

    def update(self):
        if self._world.get_picked() == self._brick:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class AtPos(BehaviorNode):
    """
    Check if brick is at position
    """

    @staticmethod
    def make(text, world, verbose=False):
        return AtPos(text, world, re.findall(r'-?\d+\.\d+|-?\d+', text), verbose)

    def __init__(self, name, world, brick_and_pos, verbose):
        self._world = world
        self._brick = int(brick_and_pos[0])
        self._pos = sm.Pos(float(brick_and_pos[1]), float(brick_and_pos[2]), float(brick_and_pos[3]))
        self._verbose = verbose
        super(AtPos, self).__init__(name)

    def update(self):
        if self._world.distance(self._brick, self._pos) < self._world.sm_par.pos_margin:
            if self._verbose:
                print(self.name, ": SUCCESS")
            return pt.common.Status.SUCCESS
        if self._verbose:
            print(self.name, ": FAILURE")
        return pt.common.Status.FAILURE


class On(BehaviorNode):
    """
    Check if one brick is on other brick
    """

    @staticmethod
    def make(text, world, verbose=False):
        return On(text, world, re.findall(r'\d+', text), verbose)

    def __init__(self, name, world, bricks, verbose):
        self._world = world
        self._upper = int(bricks[0])
        self._lower = int(bricks[1])
        self._verbose = verbose
        super(On, self).__init__(name)

    def update(self):
        if self._world.on_top(self._world.state.bricks[self._upper],
                              self._world.state.bricks[self._lower]):
            if self._verbose:
                print(self.name, ": SUCCESS")
            return pt.common.Status.SUCCESS
        if self._verbose:
            print(self.name, ": FAILURE")
        return pt.common.Status.FAILURE


class StateMachineBehavior(BehaviorNode):
    """
    Class template for state machine behaviors
    """

    def __init__(self, name, world, verbose=False):
        self._world = world
        self._state = None
        self._verbose = verbose
        super(StateMachineBehavior, self).__init__(name)

    def update(self):
        if self._verbose and self._state == pt.common.Status.RUNNING:
            print(self.name, ":", self._state)

    def success(self):
        """ Set state success """

        self._state = pt.common.Status.SUCCESS
        if self._verbose:
            print(self.name, ": SUCCESS")

    def failure(self):
        """ Set state failure """

        self._state = pt.common.Status.FAILURE
        if self._verbose:
            print(self.name, ": FAILURE")


class Pick(StateMachineBehavior):
    """
    Pick up a brick
    """

    @staticmethod
    def make(text, world, verbose=False):
        return Pick(text, world, re.findall(r'\d+', text), verbose)

    def __init__(self, name, world, brick, verbose):
        self._brick = int(brick[0])
        super(Pick, self).__init__(name, world, verbose)

    def initialise(self):
        if self._world.get_picked() == self._brick:
            self.success()
        elif self._world.get_picked() is not None:
            self.failure()
        else:
            self._state = None

    def update(self):
        super(Pick, self).update()
        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            if self._world.pick(self._brick):
                self.success()
            else:
                self.failure()
            self._world.random_event()
        return self._state


class Place(StateMachineBehavior):
    """
    Place current brick at given position
    """

    @staticmethod
    def make(text, world, verbose=False):
        if 'place at' in text:
            return Place(text, world, position=re.findall(r'-?\d+\.\d+|-?\d+', text), verbose=verbose)
        else:
            return Place(text, world, brick=re.findall(r'\d+', text), verbose=verbose)

    def __init__(self, name, world, brick=None, position=None, verbose=False):
        # pylint: disable=too-many-arguments
        if brick is not None:
            self._brick = int(brick[0])
            self._position = None
        elif position is not None:
            self._position = sm.Pos(float(position[0]), float(position[1]), float(position[2]))
            self._brick = None
        super(Place, self).__init__(name, world, verbose)

    def initialise(self):
        if self._world.get_picked() is None:
            self.failure()
        else:
            self._state = None

    def update(self):
        super(Place, self).update()

        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            if self._brick is not None:
                success = self._world.place(brick=self._brick)
            else:
                success = self._world.place(position=self._position)
            if success:
                self.success()
            else:
                self.failure()
            self._world.random_event()
        return self._state


class Put(StateMachineBehavior):
    """
    Picks brick and places it on other brick
    """

    @staticmethod
    def make(text, world, verbose=False):
        return Put(text, world, re.findall(r'-?\d+\.\d+|-?\d+', text), verbose)

    def __init__(self, name, world, brick_and_pos, verbose):
        self._brick = int(brick_and_pos[0])
        if len(brick_and_pos) > 2:
            self._position = sm.Pos(float(brick_and_pos[1]), float(brick_and_pos[2]), float(brick_and_pos[3]))
            self._lower = None
        else:
            self._lower = int(brick_and_pos[1])
            self._position = None

        super(Put, self).__init__(name, world, verbose)

    def initialise(self):
        if self._lower is not None:
            if self.world_interface.on_top(self.world_interface.state.bricks[self._brick],
                                           self.world_interface.state.bricks[self._lower]):
                self.success()
            else:
                self._state = None
        elif self._world.distance(self._brick, self._position) < self._world.sm_par.pos_margin:
            self.success()
        elif self._world.get_picked() is not None and self._world.get_picked() != self._brick:
            self.failure()
        else:
            self._state = None

    def update(self):
        super(Put, self).update()

        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            success = self._world.pick(self.brick)
            if success:
                if self._lower is not None:
                    success = self._world.place(brick=self._lower)
                else:
                    success = self._world.place(position=self._position)
            if success:
                self.success()
            else:
                self.failure()
            self._world.random_event()
        return self._state


class ApplyForce(StateMachineBehavior):
    """
    Apply force on given brick
    """

    @staticmethod
    def make(text, world, verbose=False):
        return ApplyForce(text, world, re.findall(r'\d+', text), verbose)

    def __init__(self, name, world, brick, verbose):
        self._brick = int(brick[0])
        super(ApplyForce, self).__init__(name, world, verbose)

    def initialise(self):
        if self._world.get_picked() is not None:
            self.failure()
        else:
            self._state = None

    def update(self):
        super(ApplyForce, self).update()
        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            if self._world.apply_force(self._brick):
                self.success()
            else:
                self.failure()
            self._world.random_event()
        return self._state


def get_behaviors():

    global _behavior_register

    if not _behavior_register:

        _behavior_register = BehaviorRegister()

        _behavior_register.add_condition('picked 0?', Picked)
        _behavior_register.add_condition('picked 1?', Picked)
        _behavior_register.add_condition('picked 2?', Picked)
        _behavior_register.add_action('0 at pos (0.0, 0.05, 0.0)?', AtPos)
        _behavior_register.add_action('1 at pos (0.0, 0.05, 0.0192)?', AtPos)
        _behavior_register.add_action('2 at pos (0.0, 0.05, 0.0384)?', AtPos)
        _behavior_register.add_action('0 on 1?', On)
        _behavior_register.add_action('0 on 2?', On)
        _behavior_register.add_action('1 on 0?', On)
        _behavior_register.add_action('1 on 2?', On)
        _behavior_register.add_action('2 on 0?', On)
        _behavior_register.add_action('2 on 1?', On)
        _behavior_register.add_action('pick 0!', Pick)
        _behavior_register.add_action('pick 1!', Pick)
        _behavior_register.add_action('pick 2!', Pick)
        _behavior_register.add_action('place at (0.0, 0.05, 0.0)!', Place)
        _behavior_register.add_action('place on 0!', Place)
        _behavior_register.add_action('place on 1!', Place)
        _behavior_register.add_action('place on 2!', Place)
        _behavior_register.add_action('apply force 0!', ApplyForce)
        _behavior_register.add_action('apply force 1!', ApplyForce)
        _behavior_register.add_action('apply force 2!', ApplyForce)

    return _behavior_register
