import re
import py_trees as pt
from behavior_tree_learning.sbt import BehaviorRegister, BehaviorNode
from tiago_pnp import world as sm


class BlockOnTable(BehaviorNode):
    """
    Condition checking if the cube is on table
    """

    @staticmethod
    def make(text, world, verbose=False):
        return BlockOnTable(text, world)

    def __init__(self, name, world):
        self._world = world
        super(BlockOnTable, self).__init__(name)

    def update(self):
        if self._world.feedback[sm.Feedback.CUBE] == self._world.poses.cube_goal_pose:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class IsLocalised(BehaviorNode):
    """
    Condition checking if the robot is localised
    """

    @staticmethod
    def make(text, world, verbose=False):
        return IsLocalised(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        super(IsLocalised, self).__init__(name)

    def update(self):
        if self._verbose:
            print("Checking LOC")

        if self._world.current[sm.State.LOCALISED]:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class Localise(BehaviorNode):
    """
    Localise behavior
    """

    @staticmethod
    def make(text, world, verbose=False):
        return Localise(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        self._state = None
        super(Localise, self).__init__(name)

    def initialise(self):
        if not self._world.current[sm.State.LOCALISED]:
            self._state = None

    def update(self):
        if self._verbose:
            print("LOC")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            if self._world.localise_robot():
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
        return self._state


class MoveArm(BehaviorNode):
    """
    Moving arm behavior
    """

    @staticmethod
    def make(text, world, verbose=False):

        configuration = text[text.find("[") + 1:text.find("]")]
        return MoveArm(text, world, verbose, configuration)

    def __init__(self, name, world, verbose, configuration):

        self._world = world
        self._verbose = verbose
        self._configuration = configuration
        self._state = None

        super(MoveArm, self).__init__(name)

    def initialise(self):

        if self._world.current[sm.State.ARM] != self._configuration:
            self._state = None

    def update(self):

        if self._state is None:
            self._state = pt.common.Status.RUNNING
            self._world.manipulating = True
        elif self._state is pt.common.Status.RUNNING:
            if self._world.move_arm(self._configuration):
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
            self._world.manipulating = False
        return self._state


class IsTucked(BehaviorNode):
    """
    Condition checking if the robot arm is tucked
    """

    @staticmethod
    def make(text, world, verbose=False):
        return IsTucked(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        super(IsTucked, self).__init__(name)

    def update(self):
        if self._verbose:
            print("Checking TUCK")

        # you don't want to tuck again if the robot has the cube
        if self._world.current[sm.State.ARM] == "Tucked":
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class NotHaveBlock(BehaviorNode):
    """
    Condition checking if the robot does not have the cube
    """

    @staticmethod
    def make(text, world, verbose=False):
        return NotHaveBlock(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        super(NotHaveBlock, self).__init__(name)

    def update(self):
        if self._verbose:
            print("Checking NOT BLOCK")

        if not self._world.current[sm.State.HAS_CUBE]:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class HaveBlock(BehaviorNode):
    """
    Condition checking if the robot has the cube
    """

    @staticmethod
    def make(text, world, verbose=False):
        return HaveBlock(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        super(HaveBlock, self).__init__(name)

    def update(self):
        if self._verbose:
            print("Checking PICK")
        if self._world.current[sm.State.HAS_CUBE]:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class PickUp(BehaviorNode):
    """
    Picking behavior
    """

    @staticmethod
    def make(text, world, verbose=False):
        return PickUp(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        self._state = None
        super(PickUp, self).__init__(name)

    def initialise(self):
        if self._world.feedback[sm.State.ARM] != "Pick" and not self._world.current[sm.State.HAS_CUBE]:
            self._state = None

    def update(self):
        if self._verbose:
            print("PICK")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
            self._world.manipulating = True
        elif self._state is pt.common.Status.RUNNING:
            self._world.manipulating = False
            if self._world.pick():
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE

            if self._world.current[sm.State.POSE] == self._world.poses.pick_table0:
                self._world.current[sm.State.VISITED][0] = True
            elif self._world.current[sm.State.POSE] == self._world.poses.pick_table1:
                self._world.current[sm.State.VISITED][1] = True
            elif self._world.current[sm.State.POSE] == self._world.poses.pick_table2:
                self._world.current[sm.State.VISITED][2] = True

        return self._state


class Placed(BehaviorNode):
    """
    Condition checking if the robot has placed the cube
    """

    @staticmethod
    def make(text, world, verbose=False):

        cube_id = int(re.findall(r'[0-9]+', text)[0])
        if verbose:
            print('Cube id: %d' % cube_id)
        return Placed(text, world, verbose, cube_id)

    def __init__(self, name, world, verbose, cube_id):
        self._world = world
        self._verbose = verbose
        self._cube_id = cube_id
        super(Placed, self).__init__(name)

    def update(self):
        if self._verbose:
            print("Checking PLACED")

        if (self._world.feedback[sm.Feedback.CUBE][self._cube_id] == self._world.poses.cube_goal_pose
                and not self._world.current[sm.State.HAS_CUBE]):
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class Place(BehaviorNode):
    """
    Placing behavior
    """

    @staticmethod
    def make(text, world, verbose=False):
        return Place(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        self._state = None
        super(Place, self).__init__(name)

    def initialise(self):
        if self._world.current[sm.State.HAS_CUBE]:
            self._state = None

    def update(self):
        if self._verbose:
            print("PLACE")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
            self._world.manipulating = True
        elif self._state is pt.common.Status.RUNNING:
            if self._world.place():
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
            self._world.manipulating = False
        return self._state


class Visited(BehaviorNode):
    """
    Condition checking if robot has visited a pick table and attempted the picking
    """

    @staticmethod
    def make(text, world, verbose=False):
        pose = 'xxx'
        return Visited(text, world, verbose, pose)

    def __init__(self, name, world, verbose, pose):
        self._world = world
        self._verbose = verbose
        self._pose = pose
        self._pose_idx = None
        super(Visited, self).__init__("{} visited?".format(self._pose))

    def update(self):
        if self._pose == "pick_table0":
            self._pose_idx = 0
        elif self._pose == "pick_table1":
            self._pose_idx = 1
        elif self._pose == "pick_table2":
            self._pose_idx = 2

        if self._world.current[sm.State.VISITED][self.pose_idx]:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


class MoveToPose(BehaviorNode):
    """
    Move to pose behavior
    """

    @staticmethod
    def make(text, world, verbose=False):

        if text == "move_to_pick [0]!":
            return MoveToPose(text, world, verbose, "pick_table_0")
        elif text == "move_to_pick [1]!":
            return MoveToPose(text, world, verbose, "pick_table_1")
        elif text == "move_to_pick [2]!":
            return MoveToPose(text, world, verbose, "pick_table_2")
        elif text == "move_to_place!":
            return MoveToPose(text, world, verbose, "place_table")
        else:
            raise ValueError("Unknown [%s] behavior node" % text)

    def __init__(self, name, world, verbose, pose):
        self._world = world
        self._verbose = verbose

        self._state = None
        self._pose = pose
        self._sm_pose = []

        super(MoveToPose, self).__init__(name)

    def initialise(self):

        if self._pose == "pick_table_0":
            self._sm_pose = self._world.poses.pick_table0
        elif self._pose == "pick_table_1":
            self._sm_pose = self._world.poses.pick_table1
        elif self._pose == "pick_table_2":
            self._sm_pose = self._world.poses.pick_table2
        elif self._pose == "place_table":
            self._sm_pose = self._world.poses.place_table
        elif self._pose == "random_1":
            self._sm_pose = self._world.poses.random_pose1
        elif self._pose == "random_2":
            self._sm_pose = self._world.poses.random_pose2
        elif self._pose == "random_3":
            self._sm_pose = self._world.poses.random_pose3
        elif self._pose == "random_4":
            self._sm_pose = self._world.poses.random_pose4
        elif self._pose == "random_5":
            self._sm_pose = self._world.poses.random_pose5
        elif self._pose == "random_6":
            self._sm_pose = self._world.poses.random_pose6
        elif self._pose == "random_7":
            self._sm_pose = self._world.poses.random_pose7
        elif self._pose == "random_8":
            self._sm_pose = self._world.poses.random_pose8
        elif self._pose == "random_9":
            self._sm_pose = self._world.poses.random_pose9
        elif self._pose == "origin":
            self._sm_pose = self._world.poses.origin
        elif self._pose == "spawn":
            self._sm_pose = self._world.poses.spawn_pose

        if self._world.current[sm.State.POSE] != self._sm_pose:
            self._state = None

    def update(self):
        if self._verbose:
            print("MPiT")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
            self._world.moving = True
        elif self._state is pt.common.Status.RUNNING:
            if self._world.move_to(self._sm_pose):
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
            self._world.moving = False
        return self._state


class MoveToPoseSafely(BehaviorNode):
    """
    Move to palce pose behavior taking a slower but safer path
    """

    @staticmethod
    def make(text, world, verbose=False):
        pose = 'xxx'
        return MoveToPoseSafely(text, world, verbose)

    def __init__(self, name, world, verbose, pose):

        self._world = world
        self._verbose = verbose

        self._state = None
        self._pose = pose
        self._sm_pose = []

        super(MoveToPoseSafely, self).__init__("Safely to {}!".format(self._pose))

    def initialise(self):
        if self._pose == "pick_table0":
            self._sm_pose = self._world.poses.pick_table0
        elif self._pose == "place_table":
            self._sm_pose = self._world.poses.place_table
        if self._world.current[sm.State.POSE] != self._sm_pose:
            self._state = None

    def update(self):

        if self._verbose:
            print("MPlT")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
            self._world.moving = True
        elif self._state is pt.common.Status.RUNNING:
            if self._world.move_to(self.sm_pose, safe=True):
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
            self._world.moving = False
        return self._state


class MoveHeadUp(BehaviorNode):
    """
    Move the head up behavior
    """

    @staticmethod
    def make(text, world, verbose=False):
        return MoveHeadUp(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        self._state = None
        super(MoveHeadUp, self).__init__(name)

    def initialise(self):
        if not self._world.manipulating and self._world.current[sm.State.HEAD] != 'Up':
            self._state = None

    def update(self):
        if self._verbose:
            print("UP")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            if self._world.move_head_up():
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
        return self._state


class MoveHeadDown(BehaviorNode):
    """
    Move the head down behavior
    """

    @staticmethod
    def make(text, world, verbose=False):
        return MoveHeadDown(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        self._state = None
        super(MoveHeadDown, self).__init__(name)

    def initialise(self):
        if not self._world.moving and self._world.current[sm.State.HEAD] != 'Down':
            self._state = None

    def update(self):
        if self._verbose:
            print("DOWN")

        if self._state is None:
            self._state = pt.common.Status.RUNNING
        elif self._state is pt.common.Status.RUNNING:
            if self._world.move_head_down():
                self._state = pt.common.Status.SUCCESS
            else:
                self._state = pt.common.Status.FAILURE
        return self._state


class Finished(BehaviorNode):
    """
    Condition checking if the task is finished
    """

    @staticmethod
    def make(text, world, verbose=False):
        return Finished(text, world, verbose)

    def __init__(self, name, world, verbose):
        self._world = world
        self._verbose = verbose
        super(Finished, self).__init__(name)

    def update(self):
        if self._verbose:
            print("Checking PLACED")

        cube_dist = sum(self._world.feedback[sm.Feedback.CUBE_DISTANCE])
        if cube_dist == 0.0:
            return pt.common.Status.SUCCESS
        return pt.common.Status.FAILURE


def _make_scenario1_nodes():

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('have_block?', HaveBlock)
    behavior_register.add_condition('cube_placed [0]?', Placed)
    behavior_register.add_condition('task_done?', Finished)
    behavior_register.add_action('head [Up]!', MoveHeadUp)
    behavior_register.add_action('head [Down]!', MoveHeadDown)
    behavior_register.add_action('localise!', Localise)
    behavior_register.add_action('move_to_pick [0]!', MoveToPose)
    behavior_register.add_action('move_to_place!', MoveToPose)
    behavior_register.add_action('place!', Place)
    behavior_register.add_action('pick!', PickUp)
    behavior_register.add_action('arm [Tucked]!', MoveArm)

    return behavior_register


def _make_scenario3_nodes():

    behavior_register = BehaviorRegister()
    behavior_register.add_condition('have_block?', HaveBlock)
    behavior_register.add_condition('cube_placed [0]?', Placed)
    behavior_register.add_condition('cube_placed [1]?', Placed)
    behavior_register.add_condition('cube_placed [2]?', Placed)
    behavior_register.add_condition('task_done?', Finished)
    behavior_register.add_action('head [Up]!', MoveHeadUp)
    behavior_register.add_action('head [Down]!', MoveHeadDown)
    behavior_register.add_action('localise!', Localise)
    behavior_register.add_action('move_to_pick [0]!', MoveToPose)
    behavior_register.add_action('move_to_pick [1]!', MoveToPose)
    behavior_register.add_action('move_to_pick [2]!', MoveToPose)
    behavior_register.add_action('move_to_place!', MoveToPose)
    behavior_register.add_action('place!', Place)
    behavior_register.add_action('pick!', PickUp)
    behavior_register.add_action('arm [Tucked]!', MoveArm)

    return behavior_register


def get_behaviors(name):

    if name == 'scenario_1':
        return _make_scenario1_nodes()
    elif name == 'scenario_3':
        return _make_scenario3_nodes()
    else:
        raise ValueError('Unknown %s name', name)

