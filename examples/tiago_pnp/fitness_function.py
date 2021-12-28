from dataclasses import dataclass
from tiago_pnp import world as sm


@dataclass
class Coefficients:

    # BT structure:
    depth: float = 0.0
    length: float = 0.5
    time: float = 0.1
    failure: float = 0.0
    # Task steps:
    task_completion: int = 300
    subtask: int = 100
    pick: int = 50
    # Gradient:
    cube_dist: int = 10
    localization: int = 1
    distance_robot_cube: int = 2
    robot_dist: int = 0
    min_distance_robot_cube: int = 0
    min_distance_cube_goal: int = 0


class FitnessFunction:

    def compute_cost(self, world, behavior_tree, ticks, verbose=False) -> (float, bool):

        completed = False
        coefficients = Coefficients()

        depth = behavior_tree.depth
        length = behavior_tree.length

        cube_distance = sum(world.feedback[sm.Feedback.CUBE_DISTANCE])
        min_cube_distance = sum(world.feedback[sm.Feedback.MIN_CUBE_DISTANCE])
        robot_cube_distance = sum(world.feedback[sm.Feedback.ROBOT_CUBE_DISTANCE])
        min_rc_distance = sum(world.feedback[sm.Feedback.MIN_RC_DISTANCE])

        robot_distance = world.feedback[sm.Feedback.ROBOT_DISTANCE]
        loc_error = world.feedback[sm.Feedback.LOCALIZATION_ERROR]
        time = world.feedback[sm.Feedback.ELAPSED_TIME]
        failure_probability = world.feedback[sm.Feedback.FAILURE_PB]

        cost = float(coefficients.length*length +
                     coefficients.depth*depth +
                     coefficients.cube_dist*cube_distance**2 +
                     coefficients.localization*loc_error**2 +
                     coefficients.distance_robot_cube*robot_cube_distance**2 +
                     coefficients.min_distance_cube_goal*min_cube_distance**2 +
                     coefficients.min_distance_robot_cube*min_rc_distance**2 +
                     coefficients.robot_dist*robot_distance**2 +
                     coefficients.time*time) + coefficients.failure*failure_probability

        if cube_distance == 0.0:
            completed = True
        else:
            cost += coefficients.task_completion
            for i in range(world.cubes):
                if world.feedback[sm.Feedback.CUBE_DISTANCE][i] == 0.0:
                    cost -= coefficients.subtask
                if world.current[sm.State.HAS_CUBE] and world.current[sm.State.CUBE_ID] == i:
                    cost -= coefficients.pick

        if verbose:
            print("\n")
            print("Ticks: " + str(ticks))
            print("Cube pose: " + str(world.feedback[sm.Feedback.CUBE]))
            print("Robot pose: " + str(world.feedback[sm.Feedback.AMCL]))
            print("State pose: " + str(world.current[sm.State.POSE]))
            print("\n")
            print("Cube distance from goal: " + str(cube_distance))
            print("Contribution: " + str(coefficients.cube_dist*cube_distance**2))
            print("Min cube distance: " + str(min_cube_distance))
            print("Contribution: " + str(coefficients.min_distance_cube_goal*min_cube_distance**2))
            print("Robot distance from cube: " + str(robot_cube_distance))
            print("Contribution: " + str(coefficients.distance_robot_cube*robot_cube_distance**2))
            print("Min robot distance: " + str(min_rc_distance))
            print("Contribution: " + str(coefficients.min_distance_robot_cube*min_rc_distance**2))
            print("Robot distance from goal: " + str(robot_distance))
            print("Contribution: " + str(coefficients.robot_dist*robot_distance**2))
            print("Localisation Error: " + str(loc_error))
            print("Contribution: " + str(coefficients.localization*loc_error**2))
            print("Behavior Tree: L " + str(length) + ", D " + str(depth))
            print("Contribution: " + str(coefficients.length*length + coefficients.depth*depth))
            print("Elapsed Time: " + str(time))
            print("Contribution: " + str(coefficients.time*time))
            print("Failure Probability: " + str(failure_probability))
            print("Contribution: " + str(coefficients.failure*failure_probability))
            print("Total Cost: " + str(cost))
            print("\n")

        return cost, completed
