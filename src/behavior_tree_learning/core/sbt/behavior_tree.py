"""
Class for handling string representations of behavior trees
"""
import random
import yaml

FALLBACK_NODES = []
"""
A list of all types of fallback nodes used, typically just one
"""

SEQUENCE_NODES = []
"""
A list of all types of sequence nodes used, typically just one
"""

CONTROL_NODES = []
"""
Control nodes are nodes that may have one or more children/subtrees.
Subsequent nodes will be children/subtrees until the corresponding up character is reached
List will contain FALLBACK_NODES, SEQUENCE_NODES and any other control nodes, e.g. parallel nodes
"""

CONDITION_NODES = []
"""
Conditions nodes are childless leaf nodes that never return RUNNING state.
They may never be the last child of any parent.
"""

ACTION_NODES = []
"""
Conditions nodes are also childless leaf nodes but may return RUNNING state. They may
also be the last child of any parent.
"""

ATOMIC_FALLBACK_NODES = []
"""
Atomic fallback nodes are fallback nodes that have a predetermined set of children/subtrees
that cannot be changed.  They behave mostly like action nodes except that they may not be the
children of fallback nodes. Length is counted as one.
"""

ATOMIC_SEQUENCE_NODES = []
"""
Atomic sequence nodes are sequence nodes that have a predetermined set of children/subtrees
that cannot be changed.  They behave mostly like action nodes except that they may not be the
children of sequence nodes. Length is counted as one.
"""

UP_NODE = []
"""
The up node is not really a node but a character that marks the end of a control nodes
set of children and subtrees
"""

LEAF_NODES = []
"""
CONDITIONS + ACTION_NODES + ATOMIC_FALLBACK_NODES + ATOMIC_SEQUENCE_NODES
Any kind of leaf node.
"""

BEHAVIOR_NODES = []
"""
ACTION_NODES + ATOMIC_FALLBACK_NODES + ATOMIC_SEQUENCE_NODES
Basically leaf nodes that actually do something and that may be implemented as the last child.
"""

ALL_NODES = []


def _clean_settings():

    global FALLBACK_NODES
    global SEQUENCE_NODES
    global CONTROL_NODES
    global CONDITION_NODES
    global ACTION_NODES
    global ATOMIC_FALLBACK_NODES
    global ATOMIC_SEQUENCE_NODES
    global UP_NODE
    global LEAF_NODES
    global BEHAVIOR_NODES
    global ALL_NODES

    FALLBACK_NODES = []
    SEQUENCE_NODES = []
    CONTROL_NODES = []
    CONDITION_NODES = []
    ACTION_NODES = []
    ATOMIC_FALLBACK_NODES = []
    ATOMIC_SEQUENCE_NODES = []
    LEAF_NODES = []
    BEHAVIOR_NODES = []
    UP_NODE = []
    ALL_NODES = []


def _load_settings(file_path):

    nodes = {}
    tags = ["fallback_nodes", "sequence_nodes", "condition_nodes", "action_nodes",
            "atomic_fallback_nodes", "atomic_sequence_nodes", "up_node"]

    file = file_path
    with open(file) as f:
        bt_settings = yaml.load(f, Loader=yaml.FullLoader)

    for tag in tags:
        nodes[tag] = []
        try:
            loaded_nodes = bt_settings[tag]
            if loaded_nodes is not None:
                nodes[tag] = loaded_nodes
        except KeyError:
            pass

    more_tags = ['all_nodes', 'control_nodes', 'behavior_nodes', 'leaf_nodes']
    for tag in more_tags:
        nodes[tag] = []

    nodes['control_nodes'] += nodes['fallback_nodes']
    nodes['control_nodes'] += nodes['sequence_nodes']

    nodes['behavior_nodes'] += nodes['action_nodes']
    nodes['behavior_nodes'] += nodes['atomic_fallback_nodes']
    nodes['behavior_nodes'] += nodes['atomic_sequence_nodes']

    nodes['leaf_nodes'] += nodes['condition_nodes']
    nodes['leaf_nodes'] += nodes['behavior_nodes']

    nodes['all_nodes'] += nodes['control_nodes']
    nodes['all_nodes'] += nodes['condition_nodes']
    nodes['all_nodes'] += nodes['action_nodes']
    nodes['all_nodes'] += nodes['atomic_fallback_nodes']
    nodes['all_nodes'] += nodes['atomic_sequence_nodes']
    nodes['all_nodes'] += nodes['up_node']

    return nodes


def initialize_settings():

    _clean_settings()


def add_node(type_, name):

    global FALLBACK_NODES
    global SEQUENCE_NODES
    global CONTROL_NODES
    global CONDITION_NODES
    global ACTION_NODES
    global LEAF_NODES
    global BEHAVIOR_NODES
    global UP_NODE
    global ALL_NODES

    if type_ == 'fallback':
        FALLBACK_NODES.append(name)
        CONTROL_NODES.append(name)
        ALL_NODES.append(name)
    elif type_ == 'sequence':
        SEQUENCE_NODES.append(name)
        CONTROL_NODES.append(name)
        ALL_NODES.append(name)
    elif type_ == 'condition':
        CONDITION_NODES.append(name)
        LEAF_NODES.append(name)
        ALL_NODES.append(name)
    elif type_ == 'action':
        ACTION_NODES.append(name)
        BEHAVIOR_NODES.append(name)
        LEAF_NODES.append(name)
        ALL_NODES.append(name)
    elif type_ == 'up_node':
        UP_NODE.append(name)
        ALL_NODES.append(name)


def load_settings_from_file(file_path):

    _clean_settings()
    nodes = _load_settings(file_path)

    global FALLBACK_NODES
    global SEQUENCE_NODES
    global CONTROL_NODES
    global CONDITION_NODES
    global ACTION_NODES
    global ATOMIC_FALLBACK_NODES
    global ATOMIC_SEQUENCE_NODES
    global UP_NODE
    global LEAF_NODES
    global BEHAVIOR_NODES
    global ALL_NODES

    FALLBACK_NODES = nodes['fallback_nodes']
    SEQUENCE_NODES = nodes['sequence_nodes']
    CONTROL_NODES = nodes['control_nodes']
    CONDITION_NODES = nodes['condition_nodes']
    ACTION_NODES = nodes['action_nodes']
    ATOMIC_FALLBACK_NODES = nodes['atomic_fallback_nodes']
    ATOMIC_SEQUENCE_NODES = nodes['atomic_sequence_nodes']
    UP_NODE = nodes['up_node']
    LEAF_NODES = nodes['leaf_nodes']
    BEHAVIOR_NODES = nodes['behavior_nodes']
    ALL_NODES = nodes['all_nodes']


def get_action_list():

    global ACTION_NODES
    return ACTION_NODES


class BehaviorTreeStringRepresentation:
    """
    Represent a string behavior tree (SBT), it converts a string to a string behavior tree.
    """

    def __init__(self, bt):
        """
        Creates a bt from string
        """

        self.bt = bt[:]

    def set(self, bt):
        """
        Sets bt from string
        """

        self.bt = bt[:]
        return self

    def random(self, length):
        """
        Creates a random bt of the given length
        Tries to follow some of the rules for valid trees to speed up the process
        """

        self.bt = []
        while not self.is_valid():
            if length == 1:
                self.bt = [random.choice(BEHAVIOR_NODES)]
            else:
                self.bt = [random.choice(CONTROL_NODES)]
                for _ in range(length - 1):
                    if self.bt[-1] in CONTROL_NODES:
                        child = [BehaviorTreeStringRepresentation.random_node()]
                        while child in UP_NODE:
                            child = [BehaviorTreeStringRepresentation.random_node()]
                        self.bt += child
                    else:
                        self.bt += [BehaviorTreeStringRepresentation.random_node()]

                    if self.bt[-1] in ACTION_NODES:
                        self.bt += [UP_NODE[0]]

                for _ in range(length - self.length() - 1):
                    # add nodes to match the number of individuals defined in length
                    # this is required when random node gives 'up' nodes
                    # condition nodes make it more likely to be valid
                    self.bt += [random.choice(CONDITION_NODES)]
                if self.length() < length:
                    self.bt += [random.choice(BEHAVIOR_NODES)]
                self.close()

        return self.bt

    def is_valid(self):
        """
        Checks if bt is a valid behavior tree.
        Checks are somewhat in order of likelihood to fail.
        """

        valid = True

        # Empty string
        if len(self.bt) <= 0:
            valid = False

        # The first element cannot be a leaf if after it there are other elements
        elif (self.bt[0] not in CONTROL_NODES) and (len(self.bt) != 1):
            valid = False

        else:
            for i in range(len(self.bt) - 1):

                # 'up' directly after a control node
                if (self.bt[i] in CONTROL_NODES) and (self.bt[i+1] in UP_NODE):
                    valid = False

                # Identical condition nodes directly after one another - waste
                elif self.bt[i] in CONDITION_NODES and self.bt[i] == self.bt[i+1]:
                    valid = False
                # check for non-SBT elements
                elif self.bt[i] not in ALL_NODES:
                    valid = False

            if valid:
                # Check on the bt depth: to be > 0
                depth = self.depth()
                if (depth < 0) or (depth == 0 and len(self.bt) > 1):
                    valid = False

            if valid and self.bt[0] in CONTROL_NODES:
                fallback_allowed = True
                sequence_allowed = True
                if self.bt[0] in FALLBACK_NODES:
                    fallback_allowed = False
                elif self.bt[0] in SEQUENCE_NODES:
                    sequence_allowed = False
                valid = self.is_subtree_valid(self.bt[1:], fallback_allowed, sequence_allowed)

        return valid

    def is_subtree_valid(self, string, fallback_allowed, sequence_allowed):
        # pylint: disable=too-many-return-statements, too-many-branches
        """
        Checks whether the subtree starting with string[0] is valid according to a couple rules
        1. Fallbacks must not be children of fallbacks
        2. Sequences must not be children of sequences
        """

        while len(string) > 0:
            node = string.pop(0)

            if node in UP_NODE:
                return True
            if node in ATOMIC_FALLBACK_NODES:
                if not fallback_allowed:
                    return False
            elif node in ATOMIC_SEQUENCE_NODES:
                if not sequence_allowed:
                    return False
            elif node in CONTROL_NODES:
                if node in FALLBACK_NODES:
                    if fallback_allowed:
                        if not self.is_subtree_valid(string, False, True):
                            return False
                    else:
                        return False
                elif node in SEQUENCE_NODES:
                    if sequence_allowed:
                        if not self.is_subtree_valid(string, True, False):
                            return False
                    else:
                        return False
                else:
                    if not self.is_subtree_valid(string, True, True):
                        return False

        return False

    def close(self):
        """
        Adds missing up nodes at the end, or removes from the end if too many
        """

        open_subtrees = 0

        # Make sure tree always ends with up node if starts with control node
        if len(self.bt) > 0:
            if self.bt[0] in CONTROL_NODES and self.bt[len(self.bt)-1] not in UP_NODE:
                self.bt += UP_NODE

        for node in self.bt:
            if node in CONTROL_NODES:
                open_subtrees += 1
            elif node in UP_NODE:
                open_subtrees -= 1

        if open_subtrees > 0:
            for _ in range(open_subtrees):
                self.bt += UP_NODE
        elif open_subtrees < 0:
            for _ in range(-open_subtrees):
                # Do not remove the very last node, and only up nodes
                for j in range(len(self.bt) - 2, 0, -1): # pragma: no branch, we will always find an up
                    if self.bt[j] in UP_NODE:
                        self.bt.pop(j)
                        break

    def trim(self):
        """
        Removes control nodes with only one child
        """

        for index in range(len(self.bt)-1, 0, -1):
            if self.bt[index] in CONTROL_NODES:
                children = self.find_children(index)
                if len(children) <= 1:
                    up_node_index = self.find_up_node(index)
                    self.bt.pop(up_node_index)
                    if len(children) == 1:
                        parent = self.find_parent(index)
                        if parent is not None and self.bt[parent] == self.bt[children[0]]:
                            # Parent and only child will be identical control nodes,
                            #   child can be removed
                            up_node_index = self.find_up_node(children[0])
                            self.bt.pop(up_node_index)
                            self.bt.pop(children[0])
                    self.bt.pop(index)

    def depth(self):
        """
        Returns depth of the bt
        """

        depth = 0
        max_depth = 0

        for i in range(len(self.bt)):
            if self.bt[i] in CONTROL_NODES:
                depth += 1
                max_depth = max(depth, max_depth)
            elif self.bt[i] in UP_NODE:
                depth -= 1
                if (depth < 0) or (depth == 0 and i is not len(self.bt) - 1):
                    return -1

        if depth != 0:
            return -1

        return max_depth

    def length(self):
        """
        Counts number of nodes in bt. Doesn't count up characters.
        """

        length = 0
        for node in self.bt:
            if node not in UP_NODE:
                length += 1
        return length

    @staticmethod
    def random_node():
        """
        Returns a random node.
        Usually the set of leaf nodes is much larger than the set of
        control nodes but we still typically want the final distribution to
        be approximately 50-50 between node types so this function reflects that.
        (Typically slightly more leaf nodes than control nodes, but this really depends)
        """

        if random.random() < 0.5:
            return random.choice(CONTROL_NODES)

        return random.choice(LEAF_NODES)

    def change_node(self, index, new_node=None):
        """
        Changes node at index
        """

        if self.bt[index] in UP_NODE:
            return

        if new_node is None:
            new_node = BehaviorTreeStringRepresentation.random_node()

        # Change control node to leaf node, remove whole subtree
        if new_node in LEAF_NODES and self.bt[index] in CONTROL_NODES:
            self.delete_node(index)
            self.bt.insert(index, new_node)

        # Change leaf node to control node. Add up and extra condition/behavior node child
        elif new_node in CONTROL_NODES and self.bt[index] in LEAF_NODES:
            old_node = self.bt[index]
            self.bt[index] = new_node
            if old_node in BEHAVIOR_NODES:
                self.bt.insert(index + 1, random.choice(LEAF_NODES))
                self.bt.insert(index + 2, old_node)
            else: #CONDITION_NODE
                self.bt.insert(index + 1, old_node)
                self.bt.insert(index + 2, random.choice(BEHAVIOR_NODES))
            self.bt.insert(index + 3, UP_NODE[0])
        else:
            self.bt[index] = new_node

    def add_node(self, index, new_node=None):
        """
        Adds new node at index
        """

        if new_node is None:
            new_node = BehaviorTreeStringRepresentation.random_node()
        if new_node in CONTROL_NODES:
            if index == 0:
                # Adding new control node to encapsulate entire tree
                self.bt.insert(index, new_node)
                self.bt.append(UP_NODE[0])
            else:
                self.bt.insert(index, new_node)
                self.bt.insert(index + 1, random.choice(LEAF_NODES))
                self.bt.insert(index + 2, random.choice(BEHAVIOR_NODES))
                self.bt.insert(index + 3, UP_NODE[0])
        else:
            self.bt.insert(index, new_node)

    def delete_node(self, index):
        """
        Deletes node at index
        """

        if self.bt[index] in UP_NODE:
            return

        if self.bt[index] in CONTROL_NODES:
            up_node_index = self.find_up_node(index)
            for i in range(up_node_index, index, -1):
                self.bt.pop(i)

        self.bt.pop(index)

    def find_parent(self, index):
        """
        Returns index of the closest parent to the node at input index
        """

        if index == 0:
            return None

        parent = index
        siblings_left = 0
        while parent > 0:
            parent -= 1
            if self.bt[parent] in CONTROL_NODES:
                if siblings_left == 0:
                    return parent
                siblings_left -= 1
            elif self.bt[parent] in UP_NODE:
                siblings_left += 1
        return None

    def find_children(self, index):
        """
        Finds all children to the node at index
        """

        children = []
        if self.bt[index] in CONTROL_NODES:
            child = index + 1
            level = 0
            while level >= 0:
                if self.bt[child] in UP_NODE:
                    level -= 1
                elif level == 0:
                    children.append(child)

                if self.bt[child] in CONTROL_NODES:
                    level += 1
                child += 1

        return children

    def find_up_node(self, index):
        """
        Returns index of the up node connected to the control node at input index
        """

        if self.bt[index] not in CONTROL_NODES:
            raise Exception('Invalid call. Node at index not a control node')

        if index == 0:
            if self.bt[len(self.bt)-1] in UP_NODE:
                index = len(self.bt) - 1
            else:
                raise Exception('Changing invalid SBT. Missing up.')
        else:
            level = 1
            while level > 0:
                index += 1
                if index == len(self.bt):
                    raise Exception('Changing invalid SBT. Missing up.')
                if self.bt[index] in CONTROL_NODES:
                    level += 1
                elif self.bt[index] in UP_NODE:
                    level -= 1

        return index

    def get_subtree(self, index):
        """
        Get subtree starting at index
        """

        subtree = []

        if self.bt[index] in LEAF_NODES:
            subtree = [self.bt[index]]
        elif self.bt[index] in CONTROL_NODES:
            subtree = self.bt[index : self.find_up_node(index) + 1]
        else:
            subtree = []

        return subtree

    def insert_subtree(self, subtree, index):
        """
        Insert subtree at given index
        """

        for i in range(len(subtree)):
            self.bt.insert(index + i, subtree.pop(0))

    def swap_subtrees(self, bt2, index1, index2):
        """
        Swaps two subtrees at given indices
        """

        subtree1 = self.get_subtree(index1)
        subtree2 = bt2.get_subtree(index2)

        if subtree1 != [] and subtree2 != []:
            # Remove subtrees that will be replaced
            for _ in range(len(subtree1)):
                self.bt.pop(index1)
            for _ in range(len(subtree2)):
                bt2.bt.pop(index2)

            self.insert_subtree(subtree2, index1)
            bt2.insert_subtree(subtree1, index2)

    def is_subtree(self, index):
        """
        Checks if node at index is root of a subtree
        """

        return bool(0 <= index < len(self.bt) and self.bt[index] not in UP_NODE)
