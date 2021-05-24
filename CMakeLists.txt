cmake_minimum_required(VERSION 2.8.3)
project(behavior_tree_learning)

find_package(catkin REQUIRED COMPONENTS
  roscpp rospy
)

catkin_add_nosetests(src/behavior_tree_learning/core/tests/test_py_trees_interface.py)

catkin_python_setup()
catkin_package(
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rospy
  DEPENDS
)