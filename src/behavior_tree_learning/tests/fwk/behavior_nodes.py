import py_trees as pt
from behavior_tree_learning.sbt import BehaviorRegister, BehaviorNode


class C(BehaviorNode):

    @staticmethod
    def make(text, world, _):
        return C(text, world)

    def __init__(self, name, _):
        self._name = name
        super(C, self).__init__(str(self._name))

    def update(self):
        #print(self._name)
        return pt.common.Status.SUCCESS


class A(BehaviorNode):

    @staticmethod
    def make(text, world, verbose):
        return A(text, world)

    def __init__(self, name, wold):
        super(A, self).__init__(str(name))

    def update(self):
        return pt.common.Status.SUCCESS


class Toggle1(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Toggle1(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Toggle1, self).__init__(str(name))

    def update(self):
        self._world.toggle_1()
        return pt.common.Status.SUCCESS


class Toggle2(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Toggle2(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Toggle2, self).__init__(str(name))

    def update(self):
        self._world.toggle_2()
        return pt.common.Status.SUCCESS


class Toggle3(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Toggle3(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Toggle3, self).__init__(str(name))

    def update(self):
        self._world.toggle_3()
        return pt.common.Status.SUCCESS


class Toggle4(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Toggle4(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Toggle4, self).__init__(str(name))

    def update(self):
        self._world.toggle_4()
        return pt.common.Status.SUCCESS


class Read1(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Read1(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Read1, self).__init__(str(name))

    def update(self):
        if self._world.read_1():
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class Read2(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Read2(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Read2, self).__init__(str(name))

    def update(self):
        if self._world.read_2():
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class Read3(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Read3(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Read3, self).__init__(str(name))

    def update(self):
        if self._world.read_3():
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class Read4(BehaviorNode):

    @staticmethod
    def make(text, world, verbose=False):
        return Read4(text, world)

    def __init__(self, name, world):
        self._world = world
        super(Read4, self).__init__(str(name))

    def update(self):
        if self._world.read_4():
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


def get_behaviors():

    behavior_register = BehaviorRegister()

    behavior_register.add_condition('c0', C)
    behavior_register.add_condition('c1', C)
    behavior_register.add_condition('c2', C)
    behavior_register.add_action('a0', A)
    behavior_register.add_action('a1', A)
    behavior_register.add_action('a2', A)
    behavior_register.add_action('a3', A)
    behavior_register.add_action('a4', A)
    behavior_register.add_action('a5', A)

    """
    behavior_register.add_action('t1', Toggle1)
    behavior_register.add_action('t2', Toggle1)
    behavior_register.add_action('t3', Toggle1)
    behavior_register.add_action('t4', Toggle1)
    behavior_register.add_action('r1', Read1)
    behavior_register.add_action('r2', Read2)
    behavior_register.add_action('r3', Read3)
    behavior_register.add_action('r4', Read4)
    """

    return behavior_register

