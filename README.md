# Learning Behavior Trees with Genetic Programming

This repository contains an implementation of a Genetic Programming (GP) algorithm 
that evolves Behavior Trees (BTs) to solve different tasks.

This repository is based on:
* https://github.com/jstyrud/planning-and-learning
* https://github.com/matiov/learn-BTs-with-GP

References:
* __Towards Blended Reactive Planning and Acting using Behavior Trees__.
  Colledanchise, Michele & Almeida, Diogo & Ogren, Petter.
  ICRA 2019, May 2021. DOI:10.1109/ICRA.2019.8794128. [PDF](https://arxiv.org/pdf/1611.00230.pdf)
* __A Survey of Behavior Trees in Robotics and AI__. 
  Iovino, Matteo & Scukins, Edvards & Styrud, Jonathan & Ogren, Petter & Smith, Christian. 
  May 2020. [PDF](https://arxiv.org/pdf/2005.05842.pdf)
* __Behavior Trees inRobotics and AI__.
  Colledanchise, Michele & Ogren, Petter. 
  June 2020. [PDF](https://arxiv.org/pdf/1709.00084.pdf)
* __Genetic Programming__. 
  Accessed on December 22, 2021. [Web](https://geneticprogramming.com)
* __A Field Guide to Genetic Programming__. 
  Poli, Riccardo & Langdon, William & Mcphee, Nicholas. 
  2008. ISBN 978-1-4092-0073-4.
* __Learning Behavior Trees with Genetic Programming in Unpredictable Environments__.
  Iovino, Matteo & Styrud, Jonathan & Falco, Pietro & Smith, Christian.
  ICRA 2021, May 2021. DOI:10.1109/ICRA48506.2021.9562088. [PDF](https://arxiv.org/pdf/2011.03252v1.pdf)
* __Combining Planning and Learning of Behavior Trees for Robotic Assembly__.
  Styrud, Jonathan & Iovino, Matteo & Norrlöf, Mikael & Björkman, Mårten & Smith, Christian. 
  March 2021. [PDF](https://arxiv.org/pdf/2103.09036v1.pdf) 
* __Combining Context Awareness and Planning to Learn Behavior Trees from Demonstration__. 
  Gustavsson, Oscar & Iovino, Matteo & Styrud, Jonathan & Smith, Christian. 
  September 2021. [PDF](https://arxiv.org/pdf/2109.07133.pdf)

Other references:
* __Integrating Reinforcement Learning into Behavior Trees by Hierarchical Compositio__.
  Kartašev, Mart. 
  In Degree Project Computer Sciene and Engineering, KTH, Stockholm (Sweden) 
  2019.[PDF](https://www.diva-portal.org/smash/get/diva2:1368535/FULLTEXT01.pdf)

### Installation

After cloning the repository, run the following command to install the correct dependencies:
```bash
pip3 install -r requirements.txt
```

To check the package is working well you should execute all the tests. So, move to the 
test directory of the package and execute them:
```bash
cd %PACKAGE_DIRECTORY%/src/behavior_tree_learning/tests
python -m unittest discover -s . -p 'test_*.py'
```
### Examples

Execute an existing behavior tree stored in "bt_collection.py":
```bash
cd %PACKAGE_DIRECTORY%/examples/duplo
python ./run_execute_bt.py
```

And learn a behavior tree using genetic programming: 
```bash
cd %PACKAGE_DIRECTORY%/examples/duplo
python ./run_learn_bt.py
```
