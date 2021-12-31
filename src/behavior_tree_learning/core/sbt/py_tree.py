import time
import py_trees as pt
from behavior_tree_learning.core.sbt.world import World
from behavior_tree_learning.core.sbt.behavior_tree import BehaviorTreeStringRepresentation
from behavior_tree_learning.core.sbt.node_factory import BehaviorNodeFactory


class ExecutionParameters:

    def __init__(self, max_ticks=30, max_time=30.0, max_straight_fails=1, successes_required=2):
        
        self.max_ticks = max_ticks
        self.max_time = max_time 
        self.max_straight_fails = max_straight_fails
        self.successes_required = successes_required
        

class StringBehaviorTree(pt.trees.BehaviourTree):

    class TraceInfo:

        def __init__(self, verbose):
            self.verbose = verbose

    def __init__(self, string: str, behaviors: BehaviorNodeFactory, world: World = None, root=None, verbose=False):

        if root is not None:
            self.root = root
            string = self.to_string()

        self.bt = BehaviorTreeStringRepresentation(string)
        self.depth = self.bt.depth()
        self.length = self.bt.length()
        self.failed = False
        self.timeout = False

        self._world = world
        self._behavior_factory = behaviors
        self._trace_info = self.TraceInfo(verbose)

        if root is not None:
            has_children = False
        else:
            self.root, has_children = self._behavior_factory.make_node(string[0], self._world, self._trace_info.verbose)
            string.pop(0)

        super().__init__(root=self.root)

        if has_children:
            self.create_from_string(string, self.root)

    def to_string(self):
        """
        Returns bt string (actually a list) from py tree root
        by cleaning the ascii tree from py trees
        Not complete or beautiful by any means but works for many trees
        """

        string = pt.display.ascii_tree(self.root)
        string = string.replace("[o] ", "")
        string = string.replace("\t", "")
        string = string.replace("-->", "")
        string = string.replace("Fallback", "f(")
        string = string.replace("Sequence", "s(")
        bt = string.split("\n")
        bt = bt[:-1]

        prev_leading_spaces = 999999
        for i in range(len(bt) - 1, -1, -1):
            leading_spaces = len(bt[i]) - len(bt[i].lstrip(' '))
            bt[i] = bt[i].lstrip(' ')
            if leading_spaces > prev_leading_spaces:
                for _ in range(round((leading_spaces - prev_leading_spaces) / 4)):
                    bt.insert(i + 1, ')')
            prev_leading_spaces = leading_spaces

        bt_obj = BehaviorTreeStringRepresentation(bt)
        bt_obj.close()
        
        return bt_obj.bt

    def create_from_string(self, string: str, node):
        """
        Recursive function to generate the tree from a string
        """

        while len(string) > 0:
            if string[0] == ")":
                string.pop(0)
                return node

            new_node, has_children = self._behavior_factory.make_node(string[0], self._world, self._trace_info.verbose)
            string.pop(0)
            if has_children:
                # Node is a control node or decorator with children - add subtree via string and then add to parent
                new_node = self.create_from_string(string, new_node)
                node.add_child(new_node)
            else:
                # Node is a leaf/action node - add to parent, then keep looking for siblings
                node.add_child(new_node)

        # This return is only reached if there are too few up nodes
        return node

    def run_bt(self, parameters: ExecutionParameters = ExecutionParameters()):
        """
        Function executing the behavior tree
        """

        if not self._world.startup(self._trace_info.verbose):
            return False, 0

        max_ticks = parameters.max_ticks
        max_time = parameters.max_time
        max_straight_fails = parameters.max_straight_fails
        successes_required = parameters.successes_required        
        
        ticks = 0
        straight_fails = 0
        successes = 0        
        status_ok = True
        start = time.time()

        while (self.root.status is not pt.common.Status.FAILURE or straight_fails < max_straight_fails) \
                and (self.root.status is not pt.common.Status.SUCCESS or successes < successes_required) \
                and ticks < max_ticks and status_ok:

            status_ok = self._world.is_alive()

            if status_ok:
                self.root.tick_once()

                ticks += 1
                if self.root.status is pt.common.Status.SUCCESS:
                    successes += 1
                else:
                    successes = 0

                if self.root.status is pt.common.Status.FAILURE:
                    straight_fails += 1
                else:
                    straight_fails = 0

                if time.time() - start > max_time:
                    status_ok = False
                    if self._trace_info.verbose:
                        print("Max time expired")

        if self._trace_info.verbose:
            print("Status: %s Ticks: %d, Time: %s" % (status_ok, ticks, time.time() - start))

        if ticks >= max_ticks:
            self.timeout = True
        if straight_fails >= max_straight_fails:
            self.failed = True

        self._world.shutdown()

        return status_ok, ticks

    def save_figure(self, path: str, name: str = "bt"):

        pt.display.render_dot_tree(self.root, name=name, target_directory=path)
