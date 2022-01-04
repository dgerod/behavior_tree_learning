from interface import Interface


class FitnessFunction(Interface):

    def compute_cost(self, world, behavior_tree, ticks, verbose):
        """
        Retrieve values and compute cost

        Parameters:
            world (World)
            behavior_tree (StringBehaviorTree)
            ticks (int)
            verbose (bool)
        Returns:
            cost (float)
        """
        pass

