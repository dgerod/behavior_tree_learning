"""
Implements a very simple task planner inspired from 'Towards Blended Reactive
Planning and Acting using Behavior Trees'. Generates a behaviors tree to solve
task given a set of goals and behaviors with preconditions and postconditions.
Since the conditions are not always static, it actually runs the tree while
evaluating the conditions.
"""
import py_trees as pt

from behavior_tree_learning.core.sbt import StringBehaviorTree, BehaviorNodeFactory
from behavior_tree_learning.core.sbt.behaviors import RSequence
from behavior_tree_learning.core.sbt.behavior_tree import get_action_list
from behavior_tree_learning.core.planner import PlannerBehaviorNodeFactory


def _handle_precondition(precondition, behavior_factory, world):
    """
    Handles precondition by creating a subtree whose post-conditions (aka effects)
    fulfill the pre-condition (aka condition)
    """

    print("Pre-condition in: ", precondition)
    condition_parameters = behavior_factory.get_condition_parameters(precondition)

    for action in get_action_list():
        
        action_node, _ = behavior_factory.get_node(action, world, condition_parameters)        
        if precondition in action_node.get_postconditions():
            
            action_preconditions = action_node.get_preconditions()

            if action_preconditions:

                bt = RSequence('Sequence')
                for action_precondition in action_preconditions:

                    condition_parameters = behavior_factory.get_condition_parameters(action_precondition)
                    child, _ = behavior_factory.get_node(action_precondition,
                                                         world,
                                                         condition_parameters)
                    bt.add_child(child)

                bt.add_child(action_node)

            else:
                bt = action_node

            return bt

    print("ERROR, no matching action found to ensure precondition")
    return None


def _extend_leaf_node(leaf_node, behavior_factory, world):
    """
    If leaf node fails, it should be replaced with a selector that checks leaf node
    and a subtree that fixes the pre-condition (condition) whenever it's not met.
    """

    bt = pt.composites.Selector(name='Fallback')
    leaf_node.parent.replace_child(leaf_node, bt)
    bt.add_child(leaf_node)
    print("What is failing? ", leaf_node.name)

    extended = _handle_precondition(leaf_node.name, behavior_factory, world)
    if extended is not None:
        bt.add_child(extended)


def _expand_tree(node, behavior_factory, world):
    """
    Expands the part of the tree that fails
    """

    print("TREE COMING IN :", node)

    if node.name == 'Fallback':
        print("Fallback node fails\n")
        for index, child in enumerate(node.children):
            if index >= 1:  # Normally there will only be two children
                _expand_tree(child, behavior_factory, world)

    elif node.name == 'Sequence':
        print("Sequence node fails\n")
        for i in range(len(node.children)):
            if node.children[i].status == pt.common.Status.FAILURE:
                print("Child that fails: ", node.children[i].name)
                _expand_tree(node.children[i], behavior_factory, world)
    elif isinstance(node, pt.behaviour.Behaviour) and node.status == pt.common.Status.FAILURE:

        _extend_leaf_node(node, behavior_factory, world)

    else:
        print("Tree", node.name)


def plan(world, get_execution_node, get_condition_parameters, goals):
    """
     Generates a behaviors tree to solve task given a set of goals
     and behaviors with pre-conditions and post-conditions. Since the
     conditions are not always static, it actually runs the tree while evaluating
     the conditions.
     """
    
    tree = RSequence()
    planner_behavior_factory = PlannerBehaviorNodeFactory(get_execution_node, get_condition_parameters)

    for goal in goals:

        goal_condition, _ = planner_behavior_factory.get_node(goal, world, [])
        tree.add_child(goal_condition)

    print(pt.display.unicode_tree(root=tree, show_status=True))

    for i in range(60):

        tree.tick_once()
        print("Tick: ", i)
        print(pt.display.unicode_tree(root=tree, show_status=True))

        if tree.status is pt.common.Status.FAILURE:
            _expand_tree(tree, planner_behavior_factory, world)
            print(pt.display.unicode_tree(root=tree, show_status=True))

        elif tree.status is pt.common.Status.SUCCESS:
            break

    sbt_behavior_factory = BehaviorNodeFactory(get_execution_node)
    pt.display.render_dot_tree(tree, name='Planned bt', target_directory='')
    print(StringBehaviorTree('', sbt_behavior_factory, world, tree).to_string())
