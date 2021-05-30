# Learning Behavior Trees with Genetic Programming

This repository contains an implementation of a Genetic Programming (GP) algorithm 
that evolves Behavior Trees (BTs) to solve different mobile manipulation tasks.

This repository is based on:
* https://github.com/jstyrud/planning-and-learning
* https://github.com/matiov/learn-BTs-with-GP

### Notes on installation

After cloning the repository, run the following command to install the correct dependencies:

```bash
pip3 install -r requirements.txt
```

The Behavior Tree library is based on `py-trees==0.6.8` (see 
[documentation](https://py-trees.readthedocs.io/en/devel/) and 
[repository](https://github.com/splintered-reality/py_trees/tree/release/0.6.x)), which is 
the version used by `py-tree-ros` (see 
[repository](https://github.com/splintered-reality/py_trees_ros)) for the ROS distribution 
Melodic. 

In particular, the following modifications have been made to the `py_trees` source code:
* the function `pt.display.render_dot_tree` has been modified to take as input parameter 
  the path of the target folder to save the figure;
* the function `pt.display.render_dot_tree` has been modified to display ' ' (spaces) 
  instead of * to distinguish nodes of the same type (e.g. for two Sequence nodes, the 
  first one has name 'Sequence' and the second one has name 'Sequence ' instead of 
  'Sequence*').

## Content
* `behavior_tree.py` is a class for handling string representations of behavior trees (STB).
* `behaviors.py` contains the implementation of all behaviors used in the simulations.
* `cost_function.py` is used to compute the cost function, the costs are defined here.
* `environment.py` handles the scenarios configurations and executes the SBT, returning the fitness score.
* `genetic_programming.py` implements the GP algorithm, with many possible settings.
* `gp_bt_interface.py` provides an interface between a GP algorithm and behavior tree functions.
* `hash_table.py` and `logplot.py` are utilities for data storage and visualization.

## Task description
There configuration files `.yaml` contain the list of behaviors used in the different tasks 
discussed [here](https://arxiv.org/abs/2011.03252). 

## Testing
Some BTs can be tested, to understand how they interact with the state machine simulator and to see how the fitness is computed.
To do so, run
```bash
$ pytest -s tests/test_fitness.py
```
from the repository root.
