cmake_minimum_required(VERSION 2.8.3)
project(behavior_tree_learning)

find_package(catkin REQUIRED COMPONENTS
  rospy message_generation std_msgs
)

add_service_files(FILES
    ExecuteNextGeneration.srv
    PopBehaviorTree.srv
    PushBehaviorTreeFitness.srv
)

catkin_python_setup()
catkin_package(
  LIBRARIES ${PROJECT_NAME}
  CATKIN_DEPENDS rospy message_runtime std_msgs
)
