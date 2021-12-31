from behavior_tree_learning.core.sbt.node_factory import BehaviorNodeFactory
from behavior_tree_learning.core.sbt.py_tree import StringBehaviorTree


def plot_behavior_tree(bt_name: str, sbt: str, node_factory: BehaviorNodeFactory, directory_path):

    tree = StringBehaviorTree(sbt, behaviors=node_factory, world=None)
    tree.save_figure(directory_path, name=bt_name)
